# 多用户知识专栏博客系统

本项目是软件综合实践课程项目，当前版本为 V0.5。系统定位已经从“管理员写、游客看”的个人博客，升级为“每个用户都可以建立自己的专栏、发布自己的文章、阅读和交流别人知识内容”的多用户知识创作平台。

它不是知乎、掘金或 CSDN 的仿站，也不做商业化信息流。核心是读博客、写博客、整理知识、检索知识和平等交流。

## 当前版本功能

V0.5 已实现：

- 游客浏览首页、文章、分类、标签、专栏和作者主页
- 文章标题、摘要、正文、作者和标签搜索
- 普通用户注册、登录、退出
- 普通用户编辑个人资料
- 普通用户创建和管理自己的专栏
- 普通用户发布、编辑、删除自己的文章
- 普通用户评论、点赞、收藏文章
- 同一用户不能重复点赞或收藏同一篇文章
- 用户个人中心查看文章、专栏、收藏、点赞和评论
- 管理员登录后台
- 管理员管理用户、文章、专栏、分类、标签和评论
- 普通用户不能进入后台
- AI 摘要生成、标签推荐、文章润色和文章问答接口
- AI 调用日志记录

暂未实现：

- 付费、广告、热榜、私信、关注体系
- 复杂推荐算法
- 问答社区
- Markdown 渲染
- 自动化测试套件

## 技术栈

- Python
- Flask
- Flask-Login
- Flask-SQLAlchemy
- SQLite
- Jinja2
- Bootstrap 5
- 原生 CSS

## 目录结构

```text
personal-blog-system/
├── app/
│   ├── models.py
│   ├── auth/
│   ├── user/
│   ├── column/
│   ├── article/
│   ├── public/
│   ├── admin/
│   ├── category/
│   ├── tag/
│   ├── comment/
│   ├── ai/
│   ├── dashboard/
│   ├── templates/
│   └── static/
├── docs/
├── scripts/
│   ├── init_db.py
│   └── demo_data.py
├── instance/
├── config.py
├── run.py
└── requirements.txt
```

## 日常启动

```bash
.venv/bin/python run.py
```

访问：

```text
http://127.0.0.1:5000/
```

## 首次运行

首次使用需要安装依赖并初始化数据库：

```bash
.venv/bin/pip install -r requirements.txt
.venv/bin/python scripts/init_db.py --reset
.venv/bin/python scripts/demo_data.py
.venv/bin/python run.py
```

## 测试账号

管理员：

```text
admin / admin123456
```

普通用户：

```text
alice / user123456
bob / user123456
carol / user123456
```

## 演示流程

游客流程：

1. 访问首页。
2. 浏览最新文章、推荐专栏、热门分类和热门标签。
3. 点击文章进入详情页。
4. 点击作者进入作者主页。
5. 点击专栏查看该专栏下的文章。
6. 使用搜索框搜索 `Flask` 或 `知识管理`。

普通用户流程：

1. 打开 `/login`，使用 `alice / user123456` 登录。
2. 进入个人中心 `/me`。
3. 创建自己的专栏。
4. 点击“写文章”，选择分类、标签和专栏。
5. 发布文章。
6. 打开其他用户文章，进行点赞、收藏和评论。
7. 回到个人中心查看自己的文章、收藏、点赞和评论。

管理员流程：

1. 打开 `/admin/login`，使用 `admin / admin123456` 登录。
2. 查看后台仪表盘。
3. 管理用户。
4. 管理全站文章。
5. 管理全站专栏。
6. 管理分类、标签和评论。

## 数据库初始化说明

V0.3 增加了普通用户、专栏、点赞、收藏等结构。开发演示时建议重建本地 SQLite 数据库：

```bash
.venv/bin/python scripts/init_db.py --reset
.venv/bin/python scripts/demo_data.py
```

SQLite 数据库文件位于：

```text
instance/personal_blog.sqlite
```

该文件是本地运行产物，不提交到 Git。

## AI 功能说明

完整操作步骤见：[docs/startup-and-test-guide.md](docs/startup-and-test-guide.md)。

V0.5 已接入 DeepSeek 的 OpenAI 兼容 Chat Completions 接口，默认使用 **deepseek-chat**（DeepSeek 最新旗舰模型）。

### 快速启用

```bash
export AI_API_KEY="你的 DeepSeek API Key"
.venv/bin/python run.py
```

### 6 个 AI 功能

| 功能 | 触发位置 |
|------|----------|
| 生成摘要 | 写文章页 AI 面板 |
| 推荐标签 | 写文章页 AI 面板 |
| 润色正文 | 写文章页 AI 面板 |
| 提取大纲 | 写文章页 AI 面板（v0.5 新增） |
| 标题建议 | 写文章页 AI 面板（v0.5 新增） |
| 文章问答 | 写文章页 AI 问答框 |

每个功能独立配置了温度和 max_tokens：摘要/标签/大纲使用低温度保证准确，润色/标题使用高温度增加多样性。

如果未设置 `AI_API_KEY`，页面会提示接口未配置，不会产生真实远程请求。

## 后续可扩展方向

- Markdown 渲染
- 更完整的自动化测试
- 用户修改密码
- 文章草稿预览
