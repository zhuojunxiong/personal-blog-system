import json
from dataclasses import dataclass

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
    _scene_config = {
        "summary":  (1500, 0.3),   # 摘要：低温度保证准确性
        "tags":     (800,  0.3),   # 标签：低温度保证一致性
        "polish":   (3000, 0.7),   # 润色：高温度增加表达多样性
        "chat":     (2000, 0.5),   # 问答：中等温度平衡准确与灵活
        "outline":  (2000, 0.3),   # 大纲：低温度保证结构准确
        "title":    (800,  0.7),   # 标题：高温度增加创意
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


ai_service = AIService()
