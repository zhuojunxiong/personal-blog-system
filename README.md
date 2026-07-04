# 多用户知识专栏博客系统「稷下」

> 基于 AI 辅助的个人博客系统设计与实现 —— 软件综合实践课程项目

---

## 项目简介

「稷下」是一个多用户知识专栏博客系统。每个注册用户都可以创建自己的知识专栏、发布文章、阅读和交流他人的内容。系统以"让写作回到思考，让阅读回到平等"为产品理念，围绕知识创作和知识检索构建完整的功能闭环。

当前版本：**V0.5.1**

---

## 版本演进

| 版本 | 日期 | 核心主题 |
|------|------|----------|
| V0.1 | 6/27 | 工程骨架搭建——Flask 项目结构、Blueprint 模块化、基础模板 |
| V0.2 | 6/27 | 业务闭环实现——7 类数据模型、前台浏览、后台管理、评论审核 |
| V0.3 | 6/27 | 多用户平台升级——用户注册、专栏系统、点赞收藏、定位纠偏 |
| V0.4 | 6/28 | 前端产品化重构——统一视觉系统、首页重构、DESIGN_SPEC 规范 |
| V0.4.1 | 6/28 | 交互链路收口——首页分流、个人空间、写作工作台、共享组件 |
| V0.5 | 6/29-30 | 真实 AI 接入 + 安全加固——DeepSeek 6 大 AI 功能、CSRF 保护、84 项测试 |
| **V0.5.1** | **6/30** | **AI 智能搜索 + 开箱即用——三阶段语义搜索、56 用户 133 文章、一键启动** |

详细版本迭代记录见：[项目版本迭代总结报告](../项目版本迭代总结报告.md)

---

## 当前版本功能

### 公共浏览

- 产品落地页（/）、内容首页（/home）、发现页（/discover）
- 文章列表、文章详情（阅读空间）
- 分类浏览、标签浏览
- 专栏列表、专栏详情
- 作者公共主页
- 关键词搜索、**AI 智能搜索**（自然语言语义搜索，三阶段管道）

### 用户体系

- 注册、登录、退出（支持用户名或邮箱登录）
- 个人资料编辑
- 个人空间：书房首页、知识沉淀（存档）、阅读轨迹、清谈（交流中心）、设置

### 内容创作

- 写作工作台：标题、摘要、正文、分类、专栏、标签
- 保存草稿 / 发布文章
- 编辑、删除自己的文章
- 创建、管理自己的专栏

### 互动系统

- 评论（需管理员审核后公开显示）
- 点赞（不可重复点赞同一文章）
- 收藏（不可重复收藏同一文章）
- 清谈（基于评论的轻量交流中心）

### AI 辅助（接入 DeepSeek API）

| 功能 | 说明 |
|------|------|
| 生成摘要 | 200 字结构化输出，核心观点 + 要点 + 实践价值 |
| 推荐标签 | 3-8 个技术词 + 方法词 + 场景词混合推荐 |
| 润色正文 | 修正语病、调整段落，保留标题和代码块 |
| 提取大纲 | 自动识别或归纳文章章节结构 |
| 标题建议 | 5 个候选标题：3 个务实型 + 2 个吸引型 |
| 文章问答 | 结构→论证→可读性三维度改进建议 |
| **AI 智能搜索** | 意图理解 → 关键词扩展 → 语义重排序 + 推荐理由 |

> AI 功能可配置而非强依赖：不配置 API Key 时系统照常运行，AI 按钮返回友好提示。

### 管理后台

- 仪表盘统计
- 用户管理、文章管理、专栏管理
- 分类管理、标签管理
- 评论审核（通过 / 隐藏 / 删除）
- AI 调用日志查看

### 安全机制

- 密码哈希存储（werkzeug.security）
- CSRF 全站保护（Flask-WTF，JS 自动注入方案）
- SECRET_KEY 环境变量化（否则随机生成 64 字符密钥）
- 管理员权限装饰器（普通用户无法访问后台）
- 分类下有文章时禁止删除（防数据孤儿）

---

## 技术栈

| 类别 | 技术 |
|------|------|
| 后端框架 | Python + Flask |
| 数据库 | SQLite + SQLAlchemy ORM |
| 认证 | Flask-Login |
| 安全 | Flask-WTF（CSRF） |
| 模板引擎 | Jinja2 |
| 前端 | Bootstrap 5 + 原生 CSS（v041.css）+ 原生 JS（v041.js） |
| AI | DeepSeek API（OpenAI 兼容 Chat Completions） |
| HTTP 客户端 | requests |
| 环境管理 | python-dotenv |

---

## 目录结构

```text
personal-blog-system/
├── app/
│   ├── __init__.py              # Flask 应用工厂
│   ├── extensions.py            # db, login_manager, csrf 扩展对象
│   ├── models.py                # 数据库模型（10 个模型）
│   ├── services.py              # 工具函数（utcnow, make_slug 等）
│   ├── auth/                    # 认证模块（登录/注册/退出）
│   ├── user/                    # 用户模块（个人空间/写作/设置）
│   ├── article/                 # 文章模块（查询/搜索/CRUD）
│   ├── column/                  # 专栏模块（创建/管理）
│   ├── category/                # 分类模块
│   ├── tag/                     # 标签模块
│   ├── comment/                 # 评论模块（提交/审核）
│   ├── ai/                      # AI 模块（6 大写作功能 + 智能搜索）
│   ├── admin/                   # 后台管理模块
│   ├── dashboard/               # 仪表盘模块
│   ├── public/                  # 前台公共模块
│   ├── templates/               # Jinja2 模板
│   │   ├── base.html            # 公共基础模板
│   │   ├── shared/              # 共享模板片段（6 个）
│   │   ├── v041/                # v0.4.1 页面模板
│   │   ├── public/              # 公共页面模板
│   │   ├── user/                # 用户页面模板
│   │   ├── admin/               # 后台页面模板
│   │   ├── auth/                # 认证页面模板
│   │   └── errors/              # 错误页面模板（403/404/500）
│   └── static/
│       ├── css/v041.css         # 核心样式系统（2300+ 行）
│       └── js/v041.js           # 核心交互逻辑（500+ 行）
├── docs/                        # 版本文档
│   ├── day1-development-record.md
│   ├── day2-development-record.md
│   ├── day3-development-record.md
│   ├── day4-development-record.md
│   ├── v0.4.1-design-note.md
│   ├── v0.4.1-implementation-rules.md
│   ├── v0.5-release-notes.md
│   ├── v0.5.1-release-notes.md
│   └── startup-and-test-guide.md
├── scripts/
│   ├── init_db.py               # 数据库初始化
│   └── demo_data.py             # 演示数据（56 用户 133 文章）
├── instance/                    # SQLite 数据库文件（不提交 Git）
├── config.py                    # Flask 配置
├── run.py                       # 启动入口
├── requirements.txt             # Python 依赖
├── .env.example                 # 环境变量模板
├── 启动项目.bat                  # Windows 一键启动脚本
├── AGENTS.md                    # AI 协作约束文件
├── DESIGN_SPEC.md               # 前端设计规范
├── test_e2e.py                  # 端到端测试（84 项）
├── README.md
└── .gitignore
```

---

## 快速开始

### 环境要求

- Python 3.9+
- 虚拟环境（推荐 `.venv`）

### 首次运行

```bash
# 1. 安装依赖
.venv/bin/pip install -r requirements.txt

# 2. 初始化数据库
.venv/bin/python scripts/init_db.py --reset

# 3. 加载演示数据
.venv/bin/python scripts/demo_data.py

# 4. （可选）配置 AI 功能
cp .env.example .env
# 编辑 .env，填入你的 DeepSeek API Key

# 5. 启动项目
.venv/bin/python run.py
```

Windows 用户可直接双击 `启动项目.bat`。

### 日常启动

```bash
.venv/bin/python run.py
```

访问：**http://127.0.0.1:5000/**

---

## 测试账号

| 角色 | 用户名 | 密码 |
|------|--------|------|
| 管理员 | admin | admin123456 |
| 普通用户 | alice | user123456 |
| 普通用户 | bob | user123456 |
| 普通用户 | carol | user123456 |

完整 56 个用户列表见 `scripts/demo_data.py`，所有普通用户密码均为 `user123456`。

---

## 演示流程

### 游客流程

1. 访问 `/` 查看落地页
2. 进入 `/home` 浏览最新文章和推荐专栏
3. 点击文章进入阅读页
4. 使用搜索框搜索"想学投资"体验 AI 智能搜索
5. 浏览分类、标签、专栏和作者主页

### 普通用户流程

1. 打开 `/login`，使用 alice / user123456 登录
2. 进入 `/profile` 个人书房
3. 进入 `/write` 写一篇新文章，尝试 AI 面板（摘要/标签/润色/大纲/标题/问答）
4. 发布文章
5. 打开其他用户的文章，点赞、收藏、评论
6. 回到 `/profile/archive` 查看自己的文章和专栏

### 管理员流程

1. 打开 `/admin/login`，使用 admin / admin123456 登录
2. 查看后台仪表盘统计数据
3. 管理用户、文章、专栏、分类、标签
4. 审核评论（通过 / 隐藏 / 删除）
5. 查看 AI 调用日志

---

## AI 功能配置

### 申请 API Key

1. 访问 [DeepSeek 开放平台](https://platform.deepseek.com)
2. 注册账号并创建 API Key
3. 复制 Key 到 `.env` 文件：

```bash
AI_API_KEY=sk-xxxxxxxxxxxxxxxx
```

### 可选配置

```bash
# 切换到推理模型
AI_MODEL=deepseek-reasoner

# 调整最大 token 数
AI_MAX_TOKENS=4000
```

> 未配置 API Key 时 AI 功能会提示"AI 接口未配置"，系统其他功能不受影响。

---

## 运行测试

```bash
.venv/bin/python test_e2e.py
```

84 项端到端测试覆盖：公开页面、认证流程、用户功能、权限控制、管理员功能、表单校验、搜索、边界情况。

---

## 设计规范

前端设计遵循 [DESIGN_SPEC.md](DESIGN_SPEC.md) 中定义的设计系统：

- **视觉风格**：纸质感暖色背景 + 墨水色文字 + 低视觉噪音
- **组件系统**：Header / Search Bar / Buttons / Article Card / Column Card / User Card / Tag / Category Badge / Comment Card / Auth Card / Editor Form / Empty State / Footer
- **交互状态**：所有可交互元素定义 hover / focus / active / disabled 四态
- **响应式**：桌面多列 → 平板侧栏下移 → 手机单列，禁止横向滚动

---

## 后续方向

- [ ] Markdown 渲染支持
- [ ] AI 搜索结果分页
- [ ] 文章草稿自动保存
- [ ] 真实阅读历史表
- [ ] AI 流式输出（SSE）
- [ ] 图片上传与展示
- [ ] 自动化测试扩展到 CI
- [ ] 用户关注/粉丝体系

---

## 相关仓库

- [software-practice-records](https://github.com/zhuojunxiong/software-practice-records) —— 项目过程记录仓库（需求分析、技术选型、AI 协作记录）
- 详细版本迭代总结见：[项目版本迭代总结报告](../项目版本迭代总结报告.md)

---

> 项目周期：2026 年 6 月 27 日 — 6 月 30 日
> 累计路由：67 条 | 模板文件：45+ | 数据模型：10 个 | 测试覆盖：84 项
