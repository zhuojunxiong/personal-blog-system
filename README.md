# 基于 AI 辅助的个人博客系统设计与实现

这是一个软件综合实践课程项目。当前版本为 V0.2，目标是在不接入真实 AI 接口的前提下，完成个人博客系统的基础业务闭环：前台浏览、搜索、分类标签、评论提交与审核、管理员登录、后台内容管理和基础统计。

## 技术栈

- Python
- Flask
- Flask-Login
- Flask-SQLAlchemy
- SQLite
- Jinja2
- Bootstrap
- 原生 CSS

## 当前版本：V0.2

V0.2 已实现：

- 前台首页文章列表
- 文章详情页
- 分类列表和分类文章页
- 标签列表和标签文章页
- 关键词搜索
- 游客评论提交
- 前台只展示已审核评论
- 管理员登录和退出
- 后台访问权限保护
- 后台仪表盘统计
- 文章新增、编辑、删除
- 分类新增、编辑、删除
- 标签新增、编辑、删除
- 评论审核、隐藏、删除
- 数据库初始化脚本
- 演示数据脚本
- AI 功能占位入口
- 中文 404 / 500 页面

V0.2 暂未实现：

- 真实 AI 接口
- AI 摘要生成
- AI 标签推荐
- AI 辅助写作
- 普通用户注册
- 点赞、收藏、关注、私信
- 云部署

## 目录结构

```text
personal-blog-system/
├── app/
│   ├── __init__.py
│   ├── extensions.py
│   ├── models.py
│   ├── services.py
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
├── docs/
├── instance/
├── scripts/
│   ├── init_db.py
│   └── demo_data.py
├── tests/
├── config.py
├── run.py
├── requirements.txt
└── README.md
```

## 虚拟环境

本项目使用的虚拟环境名称为：

```text
.venv
```

如果项目根目录下已经存在 `.venv`，日常启动时不需要重新创建虚拟环境，也不需要每次重新安装依赖。

## 首次运行

```powershell
cd C:\Desktop\代码\personal-blog-system
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python scripts\init_db.py
python scripts\demo_data.py
python run.py
```

启动后访问：

```text
http://127.0.0.1:5000/
```

## 日常启动

```powershell
cd C:\Desktop\代码\personal-blog-system
.\.venv\Scripts\activate
python run.py
```

## 数据库初始化

创建数据表和默认管理员：

```powershell
python scripts\init_db.py
```

插入演示分类、标签、文章和评论：

```powershell
python scripts\demo_data.py
```

SQLite 数据库保存在：

```text
instance/personal_blog.sqlite
```

该数据库文件是本地运行产物，不需要提交到 Git。

## 默认管理员账号

```text
用户名：admin
密码：admin123456
```

该账号仅用于课程演示。首次运行后请及时修改默认密码。

## 后台入口

```text
http://127.0.0.1:5000/admin/login
```

未登录用户访问后台页面时，会自动跳转到登录页。

## 基础测试

语法检查：

```powershell
.\.venv\Scripts\python.exe -m compileall app config.py run.py scripts
```

路由测试：

```powershell
$env:PYTHONIOENCODING='utf-8'
.\.venv\Scripts\python.exe -c "from app import create_app; app=create_app(); c=app.test_client(); print(c.get('/').status_code); print(c.get('/admin/dashboard').status_code)"
```

预期结果：

```text
200
302
```

含义：

- 首页可以正常访问。
- 未登录访问后台会被重定向到登录页。

## 手动验收清单

1. 访问首页，确认可以看到已发布文章。
2. 点击文章标题，进入文章详情页。
3. 刷新文章详情页，确认浏览量会增加。
4. 访问分类页，确认分类列表可见。
5. 点击分类，确认只展示该分类下已发布文章。
6. 访问标签页，确认标签云可见。
7. 点击标签，确认只展示该标签下已发布文章。
8. 使用导航栏搜索框搜索文章标题或正文关键词。
9. 在文章详情页提交评论，确认提示等待审核。
10. 登录后台，查看仪表盘统计。
11. 新增文章并选择分类和标签。
12. 编辑文章，将状态改为已发布。
13. 回到前台，确认已发布文章可见。
14. 后台新增、编辑、删除标签。
15. 后台新增、编辑、删除分类。
16. 尝试删除已有文章的分类，确认系统阻止删除。
17. 后台评论管理中审核通过待审核评论。
18. 回到文章详情页，确认审核后的评论显示。
19. 访问后台 AI 占位页面，确认不要求 API Key，也不调用真实接口。

## AI 功能说明

V0.2 不接入真实 AI 接口。`app/ai/services.py` 中仅保留以下占位函数：

- `generate_summary(content)`
- `recommend_tags(content)`
- `polish_article(content)`
- `chat_with_article(article_id, question)`

这些函数当前只返回“AI 功能将在后续版本开放”。V0.3 可以在不破坏现有博客业务的前提下替换为真实 AI 服务。

## 后续 V0.3 方向

- 接入真实 AI 摘要生成
- 接入 AI 标签推荐
- 增加 AI 操作日志页面
- 增加文章 Markdown 渲染
- 增加管理员修改密码
- 增加自动化测试
- 增加更完整的操作日志
