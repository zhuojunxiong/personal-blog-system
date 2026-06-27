# 基于 AI 辅助的个人博客系统设计与实现

这是一个软件综合实践课程项目。第一版 V0.1 的目标是先完成一个可运行、可演示、可扩展的个人博客系统骨架，再按阶段实现前台浏览、管理员后台、文章管理、分类标签、评论审核和 AI Mock 功能。

## 技术栈

- Python
- Flask
- Flask-Login
- Flask-SQLAlchemy
- SQLite
- Jinja2
- Bootstrap

## 当前阶段

已完成第一阶段：项目工程骨架。

当前包含：

- Flask app factory
- SQLAlchemy 扩展对象
- Flask-Login 扩展对象
- Public Blueprint 首页
- 基础 Jinja2 模板
- Bootstrap 页面框架
- Windows 本地运行入口

## 目录结构

```text
personal-blog-system/
├── app/
│   ├── __init__.py
│   ├── extensions.py
│   ├── auth/
│   ├── public/
│   ├── admin/
│   ├── article/
│   ├── category/
│   ├── tag/
│   ├── comment/
│   ├── ai/
│   ├── dashboard/
│   ├── templates/
│   └── static/
├── instance/
├── scripts/
├── tests/
├── config.py
├── run.py
├── requirements.txt
└── README.md
```

## 安装依赖

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

## 启动项目

```powershell
python run.py
```

启动后访问：

```text
http://127.0.0.1:5000/
```

## 第一阶段测试方式

1. 执行 `python run.py`。
2. 打开 `http://127.0.0.1:5000/`。
3. 页面能显示 “AI 辅助个人博客系统工程骨架已启动”。
4. 控制台没有导入错误或 Flask 启动错误。

## 默认管理员账号

默认管理员将在第二阶段示例数据脚本中创建：

- 用户名：`admin`
- 密码：`admin123`

密码将使用哈希保存，不会明文写入数据库。

## 后续开发顺序

1. 实现数据库模型：User、Article、Category、Tag、ArticleTag、Comment、AiLog。
2. 创建 `scripts/init_db.py` 和 `scripts/demo_data.py`。
3. 实现前台文章浏览、详情、分类、标签、搜索。
4. 实现管理员登录、退出和后台首页。
5. 实现文章、分类、标签管理。
6. 实现评论提交和审核。
7. 实现 AI Mock 摘要、标签推荐和 AI 日志。
8. 整理完整运行说明和验收测试步骤。
