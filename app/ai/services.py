import json
import re
from dataclasses import dataclass
from html import unescape
from urllib.parse import parse_qs, unquote, urlparse

import requests
from flask import current_app


class AIServiceError(RuntimeError):
    """Raised when the configured AI provider cannot complete a request."""


@dataclass
class AIResult:
    text: str
    raw: dict


class AIService:
    """AI service backed by an OpenAI-compatible chat completions API."""

    unavailable_message = "AI 接口未配置，请先设置 AI_API_KEY。"

    # ---- 每个场景的参数： (max_tokens, temperature) ----
    # DeepSeek-V3 支持最大 8K 输出，各场景按需分配以充分利用模型能力
    _scene_config = {
        "summary":  (2000, 0.3),   # 摘要：更长的摘要容纳更多要点
        "tags":     (1200, 0.3),   # 标签：更多 token 容纳更多标签候选
        "polish":   (4096, 0.7),   # 润色：长文润色需要足够输出空间
        "chat":     (3000, 0.5),   # 问答：更详细的回答
        "outline":  (3000, 0.3),   # 大纲：复杂文章需要更多层级
        "title":          (1200, 0.7),   # 标题：更多候选供选择
        "research":       (4096, 0.4),   # 资料整理：充分展开来源信息
        "search_summary": (3000, 0.3),   # 搜索摘要：更详细的文章特征提取
        "search_intent":  (1200, 0.3),   # 搜索意图：更多扩展关键词
        "search_rerank":  (3000, 0.3),   # 搜索重排：更多候选文章可处理
        "moderation":     (1200, 0.1),   # 内容审核：稳定输出 JSON 判断
        "quality":        (2500, 0.2),   # 质量诊断：结构化文章体检报告
    }

    def is_configured(self):
        return bool(current_app.config.get("AI_ENABLED") and current_app.config.get("AI_API_KEY"))

    def provider_status(self):
        if not current_app.config.get("AI_ENABLED"):
            return "AI 接口已关闭。"
        if not current_app.config.get("AI_API_KEY"):
            return self.unavailable_message
        return f"AI 接口已配置，当前模型：{current_app.config.get('AI_MODEL')}"

    # =================================================================
    # 公共方法
    # =================================================================

    def generate_summary(self, content):
        system = (
            "你是一位资深中文编辑，为知识博客平台撰写文章摘要。"
            "你的摘要需要让读者 5 秒内判断这篇文章是否值得读。\n\n"
            "要求：\n"
            "1. 第一句用一句话概括文章核心观点或解决的问题。\n"
            "2. 接着列出 3-5 条要点（用数字序号），每条不超过 30 字，覆盖文章关键内容。\n"
            "3. 最后用一句总结文章的实践价值或适用场景。\n"
            "4. 总体控制在 200 字以内，语言直接、不堆砌形容词。\n"
            "5. 不要写「本文」「作者」等套话开头。"
        )
        return self._call("summary", system, content).text

    def generate_search_summary(self, title, summary, content):
        system = (
            "你是知识写作平台的搜索摘要生成器。你的任务不是写广告文案，"
            "而是提取文章特征，帮助 AI 搜索在用户用自然语言提问时找到这篇文章。\n\n"
            "请按以下结构返回，语言简洁准确：\n"
            "核心主题：一句话说明文章讲什么。\n"
            "解决的问题：列出 2-4 个读者可能想解决的问题。\n"
            "关键知识点：列出 3-6 个具体知识点。\n"
            "可能的搜索问题：列出 3-6 个用户可能输入的问题。\n"
            "相关术语：列出有助于检索的术语，但不要做传统标签推荐。\n"
            "推荐理由：一句话说明这篇文章为什么值得读。\n\n"
            "不要夸大文章没有覆盖的内容。"
        )
        user_content = f"标题：{title}\n\n人工摘要：{summary or '无'}\n\n正文：\n{content}"
        return self._call("search_summary", system, user_content).text

    def recommend_tags(self, content):
        system = (
            "你是知识博客平台的标签专家。你的任务是阅读文章后推荐精准的标签。\n\n"
            "标签要求：\n"
            "1. 数量：3 到 8 个。\n"
            "2. 类型混合：包含 1-2 个技术/领域词（如 Flask、数据库）、"
            "1-2 个方法/概念词（如单元测试、性能优化）、1-2 个场景/用途词（如课程实践、项目复盘）。\n"
            "3. 每个标签 2-12 个中文字，不使用英文除非是公认的技术缩写。\n"
            "4. 标签应该是读者会搜索的关键词，不要太宽泛（如「技术」）也不要太冷僻。\n\n"
            "严格只返回 JSON 数组，数组元素为字符串，不要任何解释。"
        )
        result = self._call("tags", system, content).text
        return self._parse_json_list(result)

    def polish_article(self, content):
        system = (
            "你是一位资深中文写作编辑，专门帮助知识博主提升文章质量。\n\n"
            "请逐段润色以下文章，遵循以下原则：\n"
            "1. 保持原意和作者的个人风格，不做颠覆性改写。\n"
            "2. 修正语病、重复、口语化过度的表达，让句子更干净。\n"
            "3. 调整段落结构：长段落适当拆分，相邻短段落可合并，确保每段有一个明确的要点。\n"
            "4. 技术概念首次出现时可以加一句简短解释（用括号标注）。\n"
            "5. 保留原文的标题层级（# 标题、数字序号等），不改变标题文字。\n"
            "6. 如果原文有代码块或命令行，保持原样不动。\n\n"
            "直接返回润色后的全文，不要加「以下是润色后的文章」之类的说明。"
        )
        return self._call("polish", system, content).text

    def research_online(self, query):
        if not query or not query.strip():
            raise AIServiceError("请输入需要搜索的资料主题。")
        sources = self._web_search(query, limit=5)
        if not sources:
            raise AIServiceError("暂时没有获取到可用的网页资料，请换个关键词再试。")
        source_text = "\n".join(
            f"{index}. {item['title']}\n链接：{item['url']}\n摘要：{item['snippet']}"
            for index, item in enumerate(sources, start=1)
        )
        system = (
            "你是写作资料整理助手。请基于给定网页搜索结果，为作者整理可用于写文章的资料。\n\n"
            "要求：\n"
            "1. 先用 3-5 条要点总结资料共识。\n"
            "2. 再列出可写入文章的事实或角度。\n"
            "3. 保留来源链接，便于作者继续查看。\n"
            "4. 不要编造搜索结果中没有的信息。\n"
            "5. 如果来源质量参差不齐，要提醒作者继续核实。"
        )
        user_content = f"作者想查：{query}\n\n网页搜索结果：\n{source_text}"
        return self._call("research", system, user_content).text

    def chat_with_article(self, article_text, question):
        system = (
            "你是一位知识渊博的技术助教，正在帮助一位写作者理解和改进自己的文章。\n\n"
            "回答规则：\n"
            "1. 优先基于文章内容回答，明确引用文章中的相关段落或观点。\n"
            "2. 如果文章信息不足以回答问题，诚实说明，并给出 2-3 条具体的补充建议。\n"
            "3. 回答结构：先给核心结论（1-2 句），再展开说明，最后可提一个延伸思考方向。\n"
            "4. 语言友好但不啰嗦，总体控制在 400 字以内。\n"
            "5. 如果用户问的是「如何改进这篇文章」，请从结构、论证、可读性三个维度给建议。"
        )
        user_content = f"文章内容：\n{article_text}\n\n用户问题：{question}"
        return self._call("chat", system, user_content).text

    def assist_article_reading(self, title, summary, content, mode, question=""):
        mode_map = {
            "summary": (
                "请用 150 字以内总结这篇文章。先给一句核心结论，再列出 3 条关键内容。"
            ),
            "key_points": (
                "请提取这篇文章的阅读重点。用 4-6 条列表回答，每条要具体，避免空泛概括。"
            ),
            "quiz": (
                "请基于这篇文章生成 3 道复习题，并给出简短参考答案。题目要覆盖文章重点。"
            ),
            "question": (
                "请基于文章内容回答读者问题。如果文章没有足够信息，请说明不足并给出补充阅读建议。"
            ),
        }
        if mode not in mode_map:
            raise AIServiceError("不支持的 AI 阅读方式。")
        if mode == "question" and not question.strip():
            raise AIServiceError("请输入想问文章的问题。")

        system = (
            "你是知识写作平台的 AI 阅读助手。你的任务是帮助读者理解文章，"
            "不能编造文章中没有的信息。\n\n"
            "回答规则：\n"
            "1. 优先基于文章内容回答。\n"
            "2. 如果信息不足，要明确说明。\n"
            "3. 语言简洁、清楚，适合课程项目读者。\n"
            "4. 不要输出与文章无关的泛泛建议。\n\n"
            f"本次任务：{mode_map[mode]}"
        )
        user_content = (
            f"标题：{title}\n\n"
            f"摘要：{summary or '无'}\n\n"
            f"正文：\n{content}\n\n"
            f"读者问题：{question if mode == 'question' else '无'}"
        )
        return self._call("chat", system, user_content).text

    def review_article_content(self, title, summary, content):
        system = (
            "你是知识写作平台的内容审核助手。请判断文章是否疑似垃圾文章或明显不适合发布到知识平台。\n\n"
            "垃圾文章包括：广告引流、博彩色情、诈骗、恶意推广、重复灌水、无意义拼接、明显违法违规、"
            "与知识写作无关且低质量的内容。\n\n"
            "审核规则：\n"
            "1. 不要因为文章短或表达普通就轻易判定为垃圾。\n"
            "2. 如果只是质量一般但仍是正常学习笔记，应判定为 passed。\n"
            "3. 如果存在明显广告、违规或灌水风险，应判定为 suspected。\n"
            "4. reason 要具体说明判断依据，控制在 80 字以内。\n\n"
            "严格只返回 JSON 对象，格式：\n"
            '{"status": "passed 或 suspected", "reason": "审核原因", "risk_type": "normal/spam/ad/illegal/low_quality/other", "confidence": 0.0}'
        )
        user_content = f"标题：{title}\n\n摘要：{summary or '无'}\n\n正文：\n{content}"
        result = self._call("moderation", system, user_content).text
        data = self._parse_json_dict(result)
        status = data.get("status")
        if status not in ("passed", "suspected"):
            raise AIServiceError("AI 审核返回结构不符合预期。")
        return {
            "status": status,
            "reason": str(data.get("reason") or "").strip()[:500],
            "risk_type": str(data.get("risk_type") or "other").strip()[:40],
            "confidence": data.get("confidence", 0),
        }

    def evaluate_article_quality(self, title, summary, content, metrics=None):
        metrics = metrics or {}
        system = (
            "你是知识写作平台的内容质量诊断专家。请从知识文章质量和作者改进角度做体检，"
            "目标是帮助作者把文章写得更清楚、更有搜索价值，而不是替作者重写全文。\n\n"
            "诊断维度：\n"
            "1. 主题一致性：标题、摘要、正文是否围绕同一问题。\n"
            "2. 结构完整度：是否有背景、问题、步骤、总结或实践结论。\n"
            "3. 知识密度：是否包含具体概念、步骤、经验或例子。\n"
            "4. 可读性：目标读者是否容易理解。\n"
            "5. 搜索友好度：是否容易被自然语言搜索匹配到。\n"
            "6. 作者反馈：结合阅读量、点赞、收藏、评论等数据给出改进建议；如果数据很少，要说明样本不足。\n\n"
            "评分规则：score 必须是 0 到 100 的整数，60 表示基本合格，80 以上表示质量较好。\n\n"
            "严格只返回 JSON 对象，格式：\n"
            '{"score": 0-100, "audience": "适合人群", "diagnosis": "体检报告", '
            '"suggestions": ["建议1", "建议2", "建议3"], '
            '"search_advice": "搜索优化建议", "feedback": "作者反馈"}'
        )
        user_content = (
            f"标题：{title}\n\n"
            f"摘要：{summary or '无'}\n\n"
            f"当前数据：阅读量 {metrics.get('views', 0)}，"
            f"点赞 {metrics.get('likes', 0)}，收藏 {metrics.get('favorites', 0)}，"
            f"评论 {metrics.get('comments', 0)}。\n\n"
            f"正文：\n{content}"
        )
        result = self._call("quality", system, user_content).text
        data = self._parse_json_dict(result)
        try:
            score = int(data.get("score", 0))
        except (TypeError, ValueError):
            score = 0
        if 0 < score <= 10:
            score *= 10
        score = max(0, min(score, 100))
        suggestions = data.get("suggestions") or []
        if not isinstance(suggestions, list):
            suggestions = [str(suggestions)]
        return {
            "score": score,
            "audience": str(data.get("audience") or "需人工确认").strip(),
            "diagnosis": str(data.get("diagnosis") or "").strip(),
            "suggestions": [str(item).strip() for item in suggestions if str(item).strip()][:5],
            "search_advice": str(data.get("search_advice") or "").strip(),
            "feedback": str(data.get("feedback") or "").strip(),
        }

    def generate_outline(self, content):
        system = (
            "你是知识博客的结构分析师。请阅读文章后提取其大纲结构。\n\n"
            "规则：\n"
            "1. 识别文章中的所有标题和章节划分（# 标题、数字序号、分段标记等）。\n"
            "2. 用缩进列表展示层级关系，每行格式为「- 章节名」。\n"
            "3. 如果原文没有明确标题，请根据段落主题归纳出 4-8 个章节名。\n"
            "4. 每个章节名控制在 20 字以内。\n\n"
            "直接返回大纲，不要加任何前言后语。"
        )
        return self._call("outline", system, content).text

    def suggest_titles(self, content):
        system = (
            "你是知识博客的标题顾问。请基于文章内容生成 5 个候选标题。\n\n"
            "要求：\n"
            "1. 3 个偏务实型（直接说明文章解决什么问题或讲什么技术），示例风格：「Flask 多用户博客从 0 到 1 的数据库设计」。\n"
            "2. 2 个偏吸引型（用问题、对比或数字引发好奇心），示例风格：「为什么你的博客没人看？三个容易被忽略的产品细节」。\n"
            "3. 每个标题 15-40 字，适合在文章列表和搜索中展示。\n"
            "4. 每行一个标题，用数字序号开头（1. 2. 3. …）。\n\n"
            "直接返回标题列表，不要加开场白和结尾语。"
        )
        return self._call("title", system, content).text

    def search_intent_and_expand(self, query):
        """阶段1: 理解用户搜索意图并扩展关键词。
        返回 dict: {intent: str, keywords: [str], understanding: str}
        """
        system = (
            "你是一个知识博客搜索引擎的查询理解模块。你的任务是分析用户的搜索输入，"
            "理解其真实意图，并生成扩展搜索关键词。\n\n"
            "规则：\n"
            "1. 判断用户意图类型：技术学习、问题解决、经验分享、概念理解、工具推荐、其他。\n"
            "2. 提取核心概念，生成 3-8 个扩展关键词（同义词、相关术语、中英文对照）。\n"
            "3. 用一句自然语言描述你对用户查询的理解（20-50字），像是\"你想了解...\"句式。\n"
            "4. 即使用户输入不精确（如\"想学部署\"），也要推断出可能的技术方向（如 Flask 部署、云服务器部署）。\n"
            "5. 如果你不确定用户的意图，请倾向于最可能的技术方向，并在理解描述中说明你的推测。\n\n"
            "严格只返回 JSON 对象，格式：\n"
            '{"intent": "意图类型", "keywords": ["关键词1", "关键词2", ...], "understanding": "理解描述"}'
        )
        result = self._call("search_intent", system, query).text
        return self._parse_json_dict(result)

    def rerank_with_reasons(self, query, understanding, candidates):
        """阶段3: 对候选文章进行语义重排序并生成推荐理由。
        candidates: [{id, title, summary, author, tags}]
        返回: [{article_id, rank, reason, relevance}]
        """
        import json as _json
        # 精简候选数据以减少 token 消耗
        slim = []
        for c in candidates:
            slim.append({
                "id": c["id"],
                "title": c.get("title", ""),
                "summary": (c.get("ai_search_summary") or c.get("summary", "") or "")[:240],
                "author": c.get("author", ""),
                "tags": (c.get("tags") or [])[:5],
            })
        candidates_text = _json.dumps(slim, ensure_ascii=False, indent=2)
        system = (
            "你是一个知识博客的智能搜索排序助手。用户输入了搜索查询，"
            "系统根据关键词匹配找到了一些候选文章。"
            "你的任务是根据语义相关性对候选文章重新排序，并为每篇相关文章撰写推荐理由。\n\n"
            "规则：\n"
            "1. 仔细阅读用户查询和 AI 理解，判断每篇文章与用户真实需求的相关性。\n"
            "2. 只返回你认为有相关性的文章（相关性 >= 60%），无关的文章直接排除。\n"
            "3. 对每篇相关文章，按相关性从高到低排列。\n"
            "4. 为每篇文章写一句推荐理由（20-40字），说明\"为什么这篇文章可能满足你的需求\"。"
            "理由要具体，不能泛泛而谈（如\"涵盖相关主题\"太模糊，应该说\"手把手教你 Flask 部署到云服务器\"）。\n"
            "5. relevance 评分为 0.0-1.0 的浮点数。\n\n"
            "严格只返回 JSON 数组，格式：\n"
            '[{"article_id": 1, "rank": 1, "reason": "推荐理由", "relevance": 0.95}, ...]'
        )
        user_content = (
            f"用户查询：{query}\n"
            f"AI 理解：{understanding}\n"
            f"候选文章列表：\n{candidates_text}"
        )
        result = self._call("search_rerank", system, user_content).text
        return self._parse_json_list_of_dicts(result)

    def smart_search(self, query, page=1, per_page=5):
        """AI 智能搜索主入口。编排三个阶段并处理降级。
        返回: {understanding, results: [{article, reason, relevance}], total, fallback}
        """
        # 阶段1: AI 理解意图并扩展关键词
        try:
            intent_data = self.search_intent_and_expand(query)
            keywords = intent_data.get("keywords", [query])
            understanding = intent_data.get("understanding", f"您搜索了「{query}」")
        except AIServiceError:
            keywords = [query]
            understanding = f"您搜索了「{query}」"

        # 阶段2: 多关键词 SQL 搜索（最多取 20 篇候选）
        candidates = self._sql_multi_keyword_search(keywords, limit=20)

        if not candidates:
            return {"understanding": understanding, "results": [], "total": 0, "fallback": False}

        # 阶段3: AI 重排序
        try:
            ranked = self.rerank_with_reasons(query, understanding, candidates)
        except AIServiceError:
            # 降级：保持原始顺序，不加推荐理由
            paged = candidates[(page - 1) * per_page : page * per_page]
            return {
                "understanding": understanding,
                "results": [
                    {"article": c, "reason": "", "relevance": 0}
                    for c in paged
                ],
                "total": len(candidates),
                "fallback": True,
            }

        # 按 AI 排序组装结果
        ranked_map = {item["article_id"]: item for item in ranked if isinstance(item, dict)}
        final_results = []
        for c in candidates:
            if c["id"] in ranked_map:
                r = ranked_map[c["id"]]
                final_results.append({
                    "article": c,
                    "reason": r.get("reason", ""),
                    "relevance": r.get("relevance", 0),
                })

        total = len(final_results)
        paged = final_results[(page - 1) * per_page : page * per_page]
        return {
            "understanding": understanding,
            "results": paged,
            "total": total,
            "fallback": False,
        }

    @staticmethod
    def _sql_multi_keyword_search(keywords, limit=20):
        """使用多个扩展关键词进行 SQL ILIKE 搜索，合并去重。"""
        from app.models import ARTICLE_STATUS_PUBLISHED, Article, Tag, User
        from sqlalchemy import or_

        if not keywords:
            return []

        base = Article.query.filter_by(status=ARTICLE_STATUS_PUBLISHED)
        conditions = []
        for kw in keywords:
            like = f"%{kw}%"
            conditions.append(
                or_(
                    Article.title.ilike(like),
                    Article.summary.ilike(like),
                    Article.ai_search_summary.ilike(like),
                    Article.content.ilike(like),
                    Article.author.ilike(like),
                    Article.tags.any(Tag.name.ilike(like)),
                    Article.user.has(User.username.ilike(like)),
                    Article.user.has(User.nickname.ilike(like)),
                )
            )

        articles = (
            base.filter(or_(*conditions))
            .order_by(Article.published_at.desc())
            .limit(limit)
            .all()
        )

        return [
            {
                "id": a.id,
                "title": a.title,
                "slug": a.slug,
                "summary": a.summary or (a.content[:140] if a.content else ""),
                "ai_search_summary": a.ai_search_summary or "",
                "author": a.author or "",
                "author_avatar": (a.user.nickname[:1] if a.user and a.user.nickname else (a.author[:1] if a.author else "?")),
                "user_id": a.user_id,
                "tags": [t.name for t in a.tags] if a.tags else [],
                "published_at": a.published_at.isoformat() if a.published_at else "",
            }
            for a in articles
        ]

    @staticmethod
    def build_local_search_summary(title, summary, content):
        content = content or ""
        compact = " ".join(content.split())
        excerpt = compact[:420]
        parts = [
            f"核心主题：{title or '未命名文章'}",
            f"文章摘要：{summary or excerpt}",
            f"正文特征：{excerpt}",
        ]
        return "\n".join(part for part in parts if part.strip())

    @staticmethod
    def _web_search(query, limit=5):
        try:
            response = requests.get(
                "https://duckduckgo.com/html/",
                params={"q": query},
                headers={"User-Agent": "Mozilla/5.0"},
                timeout=12,
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as exc:
            raise AIServiceError(f"资料搜索暂时不可用：{exc}") from exc

        html = response.text
        items = []
        blocks = re.findall(r'<a rel="nofollow" class="result__a" href="(.*?)">(.*?)</a>', html, re.S)
        snippets = re.findall(r'<a class="result__snippet".*?>(.*?)</a>', html, re.S)
        for index, (raw_url, raw_title) in enumerate(blocks[:limit]):
            url = unescape(raw_url)
            parsed = urlparse(url)
            if parsed.path.startswith("/l/"):
                target = parse_qs(parsed.query).get("uddg", [""])[0]
                url = unquote(target) if target else url
            title = re.sub(r"<.*?>", "", unescape(raw_title)).strip()
            snippet = ""
            if index < len(snippets):
                snippet = re.sub(r"<.*?>", "", unescape(snippets[index])).strip()
            if title and url:
                items.append({"title": title, "url": url, "snippet": snippet})
        return items[:limit]

    # =================================================================
    # 内部实现
    # =================================================================

    def _call(self, scene, system_prompt, user_content):
        if not self.is_configured():
            raise AIServiceError(self.provider_status())
        if not user_content or not user_content.strip():
            raise AIServiceError("请先输入需要处理的文章内容。")

        max_tokens, temperature = self._scene_config.get(
            scene,
            (current_app.config.get("AI_MAX_TOKENS", 2000), 0.5),
        )

        base_url = current_app.config.get("AI_BASE_URL", "").rstrip("/")
        endpoint = f"{base_url}/chat/completions"
        payload = {
            "model": current_app.config.get("AI_MODEL"),
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content},
            ],
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        headers = {
            "Authorization": f"Bearer {current_app.config.get('AI_API_KEY')}",
            "Content-Type": "application/json",
        }
        try:
            response = requests.post(
                endpoint,
                json=payload,
                headers=headers,
                timeout=current_app.config.get("AI_TIMEOUT", 30),
            )
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.Timeout as exc:
            raise AIServiceError(f"AI 接口请求超时：{exc}") from exc
        except requests.exceptions.HTTPError as exc:
            detail = (exc.response.text or "")[:500]
            status_code = exc.response.status_code if exc.response is not None else "?"
            raise AIServiceError(f"AI 接口返回错误：{status_code} {detail}") from exc
        except requests.exceptions.ConnectionError as exc:
            raise AIServiceError(f"AI 接口连接失败：{exc}") from exc
        except requests.exceptions.RequestException as exc:
            raise AIServiceError(f"AI 接口请求异常：{exc}") from exc
        except ValueError as exc:
            raise AIServiceError(f"AI 接口返回内容不是有效 JSON：{exc}") from exc

        try:
            text = data["choices"][0]["message"]["content"].strip()
        except (KeyError, IndexError, TypeError) as exc:
            raise AIServiceError("AI 接口返回结构不符合预期。") from exc
        if not text:
            raise AIServiceError("AI 接口返回了空内容。")
        return AIResult(text=text, raw=data)

    @staticmethod
    def _parse_json_list(text):
        """Robustly parse a JSON array from model output, handling markdown fences."""
        clean_text = text.strip()
        if clean_text.startswith("```"):
            # Remove ```json or ``` fences
            lines = clean_text.split("\n")
            if lines and lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            clean_text = "\n".join(lines).strip()
        try:
            data = json.loads(clean_text)
        except json.JSONDecodeError:
            # Fallback: try to extract array from text
            import re
            match = re.search(r"\[.*\]", clean_text, re.DOTALL)
            if match:
                try:
                    data = json.loads(match.group(0))
                except json.JSONDecodeError:
                    return []
            else:
                return []
        if not isinstance(data, list):
            return []
        return [str(item).strip() for item in data if str(item).strip()][:8]

    @staticmethod
    def _parse_json_dict(text):
        """Parse a JSON object from model output, with markdown fence handling."""
        clean_text = text.strip()
        if clean_text.startswith("```"):
            lines = clean_text.split("\n")
            if lines and lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            clean_text = "\n".join(lines).strip()
        try:
            data = json.loads(clean_text)
            if isinstance(data, dict):
                return data
        except json.JSONDecodeError:
            import re
            match = re.search(r"\{.*\}", clean_text, re.DOTALL)
            if match:
                try:
                    data = json.loads(match.group(0))
                    if isinstance(data, dict):
                        return data
                except json.JSONDecodeError:
                    pass
        return {}

    @staticmethod
    def _parse_json_list_of_dicts(text):
        """Parse a JSON array of objects from model output, with fallback."""
        clean_text = text.strip()
        if clean_text.startswith("```"):
            lines = clean_text.split("\n")
            if lines and lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            clean_text = "\n".join(lines).strip()
        try:
            data = json.loads(clean_text)
            if isinstance(data, list):
                return [item for item in data if isinstance(item, dict)]
        except json.JSONDecodeError:
            pass
        return []


ai_service = AIService()
