# 项目启动与测试说明

当前版本：V0.5，多用户知识专栏博客系统，已接入可配置 AI 接口（DeepSeek）。

## 一、日常启动

```bash
cd "/Users/lion/Desktop/untitled folder 3/personal-blog-system"
.venv/bin/python run.py
```

浏览器打开 <http://127.0.0.1:5000/>。

**关闭服务**：在运行 `run.py` 的终端按 `Ctrl + C`。

---

## 二、启用 AI 功能

系统接入了 DeepSeek 的 OpenAI 兼容接口，支持 **6 个 AI 功能**：

| 功能 | 说明 | 触发方式 |
|------|------|----------|
| 生成摘要 | 分析文章内容，生成结构化摘要（200 字以内，含要点列表） | 写文章页 AI 面板 |
| 推荐标签 | 自动推荐 3-8 个精准中文标签，混合技术词、方法词和场景词 | 写文章页 AI 面板 |
| 润色正文 | 逐段润色，修正语病、调整结构、解释术语，保留原意和标题层级 | 写文章页 AI 面板 |
| 提取大纲 | 分析文章结构，提取或归纳章节标题（缩进列表） | 写文章页 AI 面板 |
| 标题建议 | 生成 5 个候选标题（3 个务实型 + 2 个吸引型） | 写文章页 AI 面板 |
| 文章问答 | 基于文章内容回答写作问题，支持改进建议、结构分析等 | 写文章页 AI 面板问答框 |

### 快速启用（默认最强模型）

```bash
export AI_API_KEY="你的 DeepSeek API Key"
.venv/bin/python run.py
```

系统默认使用 **deepseek-chat**（DeepSeek 最新旗舰模型），无需额外配置。

### 模型选择指南

| 模型 | 特点 | 适合 |
|------|------|------|
| `deepseek-chat`（默认） | 综合最强、指令遵循好 | 摘要、润色、问答、大纲 |
| `deepseek-reasoner` | 推理能力更强、速度较慢 | 复杂逻辑分析 |
| `deepseek-v4-flash` | 速度快、成本低 | 标签推荐等简单任务 |

切换模型：

```bash
export AI_API_KEY="你的 DeepSeek API Key"
export AI_MODEL="deepseek-reasoner"
.venv/bin/python run.py
```

### 自定义参数

```bash
export AI_API_KEY="你的 DeepSeek API Key"
export AI_MODEL="deepseek-chat"       # 模型
export AI_BASE_URL="https://api.deepseek.com"  # API 地址
export AI_MAX_TOKENS="2000"           # 默认最大输出长度
export AI_TIMEOUT="30"                # 请求超时秒数
.venv/bin/python run.py
```

不配置 `AI_API_KEY` 系统也能正常运行，AI 按钮会提示"接口未配置"。

### 申请 DeepSeek API Key

1. 打开 [DeepSeek API 平台](https://platform.deepseek.com)，登录账号。
2. 进入 API Keys 页面，创建新 Key 并复制。
3. 新用户通常有免费额度，充值后按量计费。

> ⚠️ **API Key 安全守则**：
> - 只通过终端环境变量传入，不要写进 `config.py`、README 或任何文件。
> - 不要发到聊天记录或截图分享。
> - 如果已泄露，立即去 DeepSeek 后台删除该 Key 并重新生成。

---

## 三、AI 功能使用教程

### 使用流程

1. 注册/登录普通用户账号。
2. 点击导航栏"写文章"进入写作空间。
3. 输入标题和正文内容。
4. 右侧 AI 面板点击对应按钮：

```
┌──────────────────────────────────────────────────────────┐
│  写作空间                                        Assistant │
│                                                            │
│  ┌──────────────────────────┐  ┌────────────────────────┐  │
│  │  标题：______________   │  │  [生成摘要] [推荐标签] │  │
│  │                          │  │  [润色正文] [提取大纲] │  │
│  │  正文：                  │  │  [标题建议]            │  │
│  │  ____________________   │  │                        │  │
│  │  ____________________   │  │  ── AI 问答 ──         │  │
│  │  ____________________   │  │  [我想问…]     [发送]  │  │
│  │                          │  │                        │  │
│  └──────────────────────────┘  └────────────────────────┘  │
│  [保存草稿]  [发布文章]                                    │
└──────────────────────────────────────────────────────────┘
```

### 各功能最佳实践

**生成摘要**：先写好正文（至少 200 字以上），再点生成。AI 会根据实际内容生成结构化摘要，包括核心观点、3-5 条要点和实践价值。生成后自动填入摘要框，你可以再手动微调。

**推荐标签**：AI 会推荐技术/领域词、方法/概念词、场景/用途词的混合列表。系统会自动勾选已有的匹配标签。对于新出现的标签名，你需要先去后台创建。

**润色正文**：点击后 AI 逐段润色并替换编辑区内容。如果对结果不满意，可以再次点击润色（每次都会重新处理），或手动修改。建议润色后再通读一遍。

**提取大纲**：AI 分析文章结构后在问答区显示大纲。如果原文有 `# 标题` 或数字序号，会直接识别；如果没有，AI 会根据段落主题归纳。适合写完初稿后检查结构是否合理。

**标题建议**：AI 生成 5 个候选标题显示在问答区。前 3 个偏务实（直接说明内容），后 2 个偏吸引（用问题或对比引发好奇）。可以从中选取满意的复制到标题框。

**文章问答**：在问答框里输入问题，AI 会基于文章内容回答。支持的提问类型：
- 结构分析："我这篇文章的结构合理吗？"
- 改进建议："如何让这篇教程更容易理解？"
- 内容补充："这个话题还缺少哪些关键技术点？"
- 概念解释："文中的 XX 概念解释清楚了吗？"

---

## 四、重新构建数据库

如果页面报数据库字段或表不存在：

```bash
.venv/bin/python scripts/init_db.py --reset
.venv/bin/python scripts/demo_data.py
```

> `--reset` 会清空本地数据库，仅用于开发演示。

---

## 五、测试账号

| 角色 | 用户名 | 密码 |
|------|--------|------|
| 管理员 | admin | admin123456 |
| 普通用户 | alice | user123456 |
| 普通用户 | bob | user123456 |
| 普通用户 | carol | user123456 |

---

## 六、基础自动测试

语法检查：

```bash
.venv/bin/python -m compileall app config.py run.py scripts
```

路由快速测试：

```bash
.venv/bin/python -c "from app import create_app; app=create_app(); c=app.test_client(); print(c.get('/').status_code); print(c.get('/columns').status_code); print(c.get('/admin/dashboard').status_code)"
```

预期输出：

```text
200
200
302
```

---

## 七、手动验收流程

### 游客
1. 访问首页 → 看到落地页，可进入文章、分类、标签、专栏浏览。
2. 使用搜索框搜索文章 → 搜索页展示文章、专栏、作者结果。
3. 点击作者进入作者主页。
4. 未登录时点赞、收藏或评论 → 跳转登录页。

### 普通用户（AI 功能测试）
1. 使用 `alice / user123456` 登录。
2. 进入个人中心 → 创建专栏。
3. 点击"写文章"，输入标题和正文（至少 200 字）。
4. 依次测试 AI 面板的 5 个按钮：生成摘要、推荐标签、润色正文、提取大纲、标题建议。
5. 在问答框输入"这篇文章可以如何改进？"并发送。
6. 选择分类、标签、专栏后发布文章。
7. 编辑或删除自己的文章。
8. 点赞、收藏、评论其他用户文章。
9. 在个人中心查看互动记录。

### 管理员
1. 使用 `admin / admin123456` 登录后台 `/admin/login`。
2. 查看仪表盘。
3. 管理用户、文章、专栏、分类、标签和评论。
4. 查看 AI 接口状态 `/admin/ai`。
5. 用普通用户账号访问 `/admin` → 被拒绝。

---

## 八、常见问题

### 服务关不掉
在运行 `run.py` 的终端按 `Ctrl + C`。如果终端已关闭，用以下命令找到并终止进程：
```bash
lsof -i :5000 | grep LISTEN
kill -9 <PID>
```

### 页面提示"AI 接口未配置"
说明当前终端没有设置 `AI_API_KEY`。在**同一个终端**里先设置再启动：
```bash
export AI_API_KEY="你的 DeepSeek API Key"
.venv/bin/python run.py
```

### AI 返回内容质量不高
可能原因及解决：
1. **模型太弱**：确认使用的是 `deepseek-chat`（默认），不是 `deepseek-v4-flash`。
2. **正文太短**：至少写 200 字以上，AI 需要足够上下文才能产生有意义的输出。
3. **问题太模糊**：问答时尽量具体，如"本文逻辑结构怎么样"比"帮我看看"更好。

### AI 接口返回错误
常见原因：API Key 写错、DeepSeek 账号余额不足、网络不通。

确认环境变量：
```bash
echo $AI_API_KEY
```
> 不要将输出截图或发送给他人。

### 缺少依赖
```bash
.venv/bin/pip install -r requirements.txt
```

### 端口 5000 被占用
```bash
.venv/bin/python -c "from app import create_app; app = create_app(); app.run(debug=True, port=5001)"
```
然后访问 `http://127.0.0.1:5001/`。

### 数据库表不存在
```bash
.venv/bin/python scripts/init_db.py --reset
.venv/bin/python scripts/demo_data.py
```

---

## 九、注意事项

- 不要把 API Key 写进 `config.py`、README 或任何文档。
- 不要把 `instance/personal_blog.sqlite` 当作正式线上数据库。
- 不要把 `.venv` 提交到 Git（已在 `.gitignore` 中排除）。
- API Key 在**每个新终端**都需要重新 export，关闭终端后失效。
