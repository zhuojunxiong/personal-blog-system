# 第一天开发记录：项目骨架搭建

## 一、基本信息

- 项目名称：基于 AI 辅助的个人博客系统设计与实现
- 开发日期：2026 年 6 月 27 日
- 当前版本：V0.1 第一阶段
- 当前目标：完成可运行、可演示、可扩展的 Flask 项目工程骨架

## 二、今天的开发目标

第一天没有直接实现完整业务功能，而是先完成项目的基础工程结构。这样做的目的是先保证项目可以启动、模块边界清楚，后续再逐步增加数据库模型、前台浏览、后台管理、评论审核和 AI Mock 功能。

今天重点完成以下内容：

1. 明确第一版 V0.1 的功能边界。
2. 创建 Flask 项目目录结构。
3. 使用 app factory 方式创建 Flask 应用。
4. 配置 Flask-SQLAlchemy 和 Flask-Login 扩展对象。
5. 创建 Public Blueprint，并实现一个首页测试页面。
6. 创建基础 Jinja2 模板和简单样式。
7. 编写 `requirements.txt`、`run.py`、`config.py`。
8. 编写项目说明文档 `README.md`。
9. 补充 `AGENTS.md`，记录后续开发约束。
10. 完成第一阶段运行验证。

## 三、今天完成的文件

### 1. 项目说明与工程约束

- `README.md`
  - 记录项目简介、技术栈、目录结构、安装方式、启动方式、当前阶段和后续计划。

- `AGENTS.md`
  - 记录项目长期开发约束。
  - 明确项目必须模块化开发。
  - 明确不能做普通用户注册、复杂社区、前后端分离和真实 AI 接口强依赖。

- `.gitignore`
  - 忽略 `.venv/`、`__pycache__/`、本地 SQLite 数据库、测试缓存等临时文件。

### 2. Flask 启动与配置文件

- `run.py`
  - 项目本地启动入口。
  - 执行 `python run.py` 后可以启动 Flask 开发服务器。

- `config.py`
  - 保存 Flask 配置。
  - 当前配置了 `SECRET_KEY`、SQLite 数据库路径和 SQLAlchemy 参数。

- `requirements.txt`
  - 记录当前阶段依赖：
    - Flask
    - Flask-Login
    - Flask-SQLAlchemy

### 3. Flask 应用核心文件

- `app/__init__.py`
  - 使用 app factory 模式创建 Flask 应用。
  - 初始化数据库扩展和登录扩展。
  - 注册 Blueprint。
  - 当前先注册了 public 前台模块。

- `app/extensions.py`
  - 集中创建扩展对象：
    - `db`
    - `login_manager`
  - 这样可以避免后续模块之间循环导入。

### 4. 前台模块

- `app/public/__init__.py`
  - 标记 public 为前台游客模块。

- `app/public/routes.py`
  - 创建 `public_bp` 蓝图。
  - 实现首页路由 `/`。

### 5. 模板与静态资源

- `app/templates/base.html`
  - 项目基础模板。
  - 包含页面头部、导航栏、主体内容块和页脚。
  - 引入 Bootstrap 和自定义 CSS。

- `app/templates/public/index.html`
  - 当前阶段首页。
  - 用于验证 Flask 模板、路由和 Blueprint 是否正常工作。

- `app/static/css/main.css`
  - 当前阶段基础样式文件。

### 6. 预留模块目录

今天还创建了以下模块目录，为后续开发做准备：

- `app/auth/`
  - 后续用于管理员登录和退出。

- `app/admin/`
  - 后续用于后台首页和后台权限控制。

- `app/article/`
  - 后续用于文章新增、编辑、删除和状态管理。

- `app/category/`
  - 后续用于分类管理。

- `app/tag/`
  - 后续用于标签管理。

- `app/comment/`
  - 后续用于游客评论提交和管理员评论审核。

- `app/ai/`
  - 后续用于 AI Mock 摘要生成、标签推荐和 AI 日志记录。

- `app/dashboard/`
  - 后续用于后台统计信息。

- `scripts/`
  - 后续用于数据库初始化脚本和演示数据脚本。

- `tests/`
  - 后续用于测试代码。

- `instance/`
  - 后续用于保存本地 SQLite 数据库。

## 四、当前项目框架结构

```text
personal-blog-system/
├── AGENTS.md
├── README.md
├── LICENSE
├── .gitignore
├── config.py
├── run.py
├── requirements.txt
├── app/
│   ├── __init__.py
│   ├── extensions.py
│   ├── auth/
│   │   └── __init__.py
│   ├── admin/
│   │   └── __init__.py
│   ├── article/
│   │   └── __init__.py
│   ├── category/
│   │   └── __init__.py
│   ├── tag/
│   │   └── __init__.py
│   ├── comment/
│   │   └── __init__.py
│   ├── ai/
│   │   └── __init__.py
│   ├── dashboard/
│   │   └── __init__.py
│   ├── public/
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── public/
│   │   │   └── index.html
│   │   ├── admin/
│   │   └── auth/
│   └── static/
│       ├── css/
│       │   └── main.css
│       ├── js/
│       └── uploads/
├── instance/
├── scripts/
├── tests/
└── docs/
    └── day1-development-record.md
```

## 五、项目模块设计说明

当前项目采用模块化 Flask 结构，后续功能会通过 Blueprint 拆分。整体思路是：

- `app/__init__.py`
  - 只负责创建 Flask 应用、初始化扩展、注册蓝图。

- `app/extensions.py`
  - 只负责保存第三方扩展对象。

- `app/models.py`
  - 下一阶段创建，用于保存数据库模型。

- `auth` 模块
  - 负责管理员登录、退出和登录状态管理。

- `public` 模块
  - 负责游客访问功能，包括首页、文章详情、分类浏览、标签浏览和搜索。

- `admin` 模块
  - 负责后台首页和后台访问权限控制。

- `article` 模块
  - 负责文章后台管理，包括新增、编辑、删除、发布、下架等功能。

- `category` 模块
  - 负责分类增删改查。

- `tag` 模块
  - 负责标签增删改查。

- `comment` 模块
  - 负责游客评论提交和管理员审核。

- `ai` 模块
  - 负责 AI Mock 功能，包括摘要生成、标签推荐和 AI 操作日志。

- `dashboard` 模块
  - 负责后台统计信息。

## 六、当前运行方式

### 1. 创建虚拟环境

```powershell
python -m venv .venv
```

### 2. 激活虚拟环境

```powershell
.\.venv\Scripts\activate
```

### 3. 安装依赖

```powershell
pip install -r requirements.txt
```

### 4. 启动项目

```powershell
python run.py
```

启动后访问：

```text
http://127.0.0.1:5000/
```

## 七、第一天验证结果

今天已经完成以下验证：

1. Python 语法检查通过。
2. Flask 应用可以正常创建。
3. 首页路由 `/` 可以访问。
4. 首页返回状态码为 `200`。
5. 页面可以正常渲染基础模板和首页内容。

当前首页显示内容为：

```text
AI 辅助个人博客系统工程骨架已启动
```

这说明第一阶段项目骨架已经具备继续开发的基础。

## 八、当前尚未实现的功能

第一天只完成工程骨架，以下功能还没有实现：

1. 数据库模型。
2. 数据库初始化脚本。
3. 示例数据脚本。
4. 管理员账号创建。
5. 前台文章列表和文章详情。
6. 分类、标签和搜索功能。
7. 管理员登录。
8. 后台文章管理。
9. 评论提交和审核。
10. AI Mock 摘要生成和标签推荐。
11. AI 日志查看。

这些内容会在后续阶段逐步实现。

## 九、下一步开发计划

第二阶段建议实现数据库模型和初始化脚本，具体包括：

1. 创建 `app/models.py`。
2. 实现 `User`、`Article`、`Category`、`Tag`、`ArticleTag`、`Comment`、`AiLog` 七类数据模型。
3. 创建 `scripts/init_db.py`，用于初始化数据库。
4. 创建 `scripts/demo_data.py`，用于插入演示数据。
5. 创建默认管理员账号：
   - 用户名：`admin`
   - 密码：`admin123`
6. 确保密码使用哈希保存，不能明文保存。

第二阶段完成后，项目就可以进入前台文章浏览功能开发。
