# 第二天开发记录：V0.2 业务闭环实现

## 一、基本信息

- 项目名称：基于 AI 辅助的个人博客系统设计与实现
- 开发日期：2026 年 6 月 27 日
- 当前版本：V0.2
- 开发目标：在 V0.1 工程骨架基础上，实现除 AI 功能之外的博客基础业务闭环

## 二、第二天开发目标

V0.1 只完成了项目骨架。第二天的重点是把系统推进到可以演示和验收的状态。

本次开发明确不接入真实 AI 接口，不要求 API Key，也不实现 AI 摘要、AI 推荐或 AI 问答。AI 相关内容只保留模块和后台占位，方便 V0.3 继续扩展。

本次主要完成：

1. 数据库模型。
2. 数据库初始化脚本。
3. 演示数据脚本。
4. 前台文章展示。
5. 文章详情。
6. 分类和标签浏览。
7. 搜索功能。
8. 评论提交和审核。
9. 管理员登录和退出。
10. 后台仪表盘。
11. 文章、分类、标签、评论管理。
12. AI 功能占位。
13. 前后台页面样式优化。
14. README 和启动文档更新。

## 三、本次新增的核心文件

### 1. 数据模型

- `app/models.py`
  - 新增 `User`、`Article`、`Category`、`Tag`、`ArticleTag`、`Comment`、`AiLog`。
  - 文章状态包括 `draft` 和 `published`。
  - 评论状态包括 `pending`、`approved` 和 `hidden`。
  - 用户密码使用哈希存储。
  - 文章和标签使用多对多关系。

### 2. 业务服务层

- `app/article/services.py`
  - 文章查询、搜索、新增、编辑、删除、浏览量增加。

- `app/category/services.py`
  - 分类查询、新增、编辑、删除。
  - 分类下存在文章时禁止删除。

- `app/tag/services.py`
  - 标签查询、新增、编辑、删除。
  - 删除标签时同步清理文章标签关系。

- `app/comment/services.py`
  - 评论提交、校验、审核、隐藏、删除。

- `app/dashboard/services.py`
  - 后台统计数据。

- `app/ai/services.py`
  - AI 功能占位函数。
  - 当前只返回“AI 功能将在后续版本开放”。

### 3. 路由模块

- `app/public/routes.py`
  - 首页、文章详情、分类、标签、搜索。

- `app/auth/routes.py`
  - 管理员登录和退出。

- `app/admin/routes.py`
  - 后台入口跳转。

- `app/dashboard/routes.py`
  - 后台仪表盘。

- `app/article/routes.py`
  - 后台文章管理。

- `app/category/routes.py`
  - 后台分类管理。

- `app/tag/routes.py`
  - 后台标签管理。

- `app/comment/routes.py`
  - 前台评论提交和后台评论管理。

- `app/ai/routes.py`
  - AI 占位页面。

### 4. 模板文件

新增前台模板：

- `app/templates/public/_article_card.html`
- `app/templates/public/_pagination.html`
- `app/templates/public/article_detail.html`
- `app/templates/public/categories.html`
- `app/templates/public/category_detail.html`
- `app/templates/public/tags.html`
- `app/templates/public/tag_detail.html`
- `app/templates/public/search.html`

新增后台模板：

- `app/templates/admin/base.html`
- `app/templates/admin/dashboard.html`
- `app/templates/admin/articles/index.html`
- `app/templates/admin/articles/form.html`
- `app/templates/admin/categories/index.html`
- `app/templates/admin/categories/form.html`
- `app/templates/admin/tags/index.html`
- `app/templates/admin/tags/form.html`
- `app/templates/admin/comments/index.html`
- `app/templates/admin/ai/index.html`

新增认证和错误页面：

- `app/templates/auth/login.html`
- `app/templates/errors/404.html`
- `app/templates/errors/500.html`

### 5. 数据脚本

- `scripts/init_db.py`
  - 创建数据表。
  - 创建默认管理员。
  - 创建默认分类。

- `scripts/demo_data.py`
  - 创建演示分类。
  - 创建演示标签。
  - 创建演示文章。
  - 创建演示评论。
  - 创建 AI 占位日志。

## 四、本次修改的核心文件

- `app/__init__.py`
  - 注册所有 Blueprint。
  - 配置 Flask-Login 用户加载。
  - 增加 404 和 500 中文错误页。
  - 增加分页链接模板 helper。

- `app/templates/base.html`
  - 从 V0.1 基础页面升级为 V0.2 前台公共布局。
  - 增加首页、分类、标签、搜索和后台入口导航。

- `app/static/css/main.css`
  - 增加前台 Apple 风格的留白、卡片、层级、轻交互和响应式布局。
  - 增加后台侧边栏、统计卡片、表格和表单样式。

- `README.md`
  - 更新为 V0.2 运行说明、初始化说明、默认账号、功能清单和验收清单。

- `docs/startup-and-test-guide.md`
  - 更新为 V0.2 启动和测试说明。
  - 明确虚拟环境名称为 `.venv`。

## 五、实现的前台功能

1. 首页展示已发布文章。
2. 首页文章卡片展示标题、摘要、分类、标签、作者、发布时间、浏览量和评论数。
3. 首页分页。
4. 文章详情页。
5. 文章详情页浏览量增加。
6. 分类列表。
7. 分类文章列表。
8. 标签列表。
9. 标签文章列表。
10. 搜索标题、摘要和正文。
11. 游客提交评论。
12. 评论提交后默认待审核。
13. 前台只展示审核通过的评论。
14. 中文 404 和 500 页面。

## 六、实现的后台功能

1. 管理员登录。
2. 管理员退出。
3. 后台访问权限保护。
4. 后台仪表盘统计。
5. 文章列表。
6. 新增文章。
7. 编辑文章。
8. 删除文章。
9. 文章草稿和发布状态。
10. 分类新增、编辑、删除。
11. 分类下存在文章时禁止删除。
12. 标签新增、编辑、删除。
13. 删除标签时清理文章标签关系。
14. 评论列表。
15. 评论审核通过。
16. 评论隐藏。
17. 评论删除。
18. AI 功能占位页面。

## 七、权限和校验

权限控制：

- 后台页面全部使用 `login_required`。
- 未登录访问后台会跳转到 `/admin/login`。
- 登录失败会显示中文错误提示。

表单校验：

- 文章标题不能为空。
- 文章正文不能为空。
- 文章必须选择分类。
- 文章状态必须合法。
- 分类名称不能为空且不能重复。
- 标签名称不能为空且不能重复。
- 评论昵称不能为空。
- 评论邮箱格式必须合理。
- 评论内容不能为空且限制长度。

## 八、前端设计说明

前台页面参考 Apple 风格的设计原则，但没有复制 Apple 官网内容、图片、商标或文案。

具体体现：

1. 大面积留白。
2. 清晰的标题层级。
3. 克制的颜色使用。
4. 卡片式文章列表。
5. 柔和阴影。
6. 轻量 hover 动效。
7. 响应式布局。
8. 文章详情页正文宽度适中，便于阅读。

后台页面偏管理系统风格，重点是清晰、稳定、易操作。

## 九、后端严谨性说明

本次开发参考流程型系统的严谨思路，重点体现在：

1. 文章和评论状态清晰。
2. 后台访问必须登录。
3. 评论提交后不能直接展示。
4. 分类下有文章时不能误删。
5. 删除文章会同步处理评论和标签关系。
6. 搜索空关键词不会导致异常。
7. 数据初始化可复现。
8. 关键操作都有中文提示。

## 十、运行方式

如果 `.venv` 已存在：

```powershell
cd C:\Desktop\代码\personal-blog-system
.\.venv\Scripts\activate
python scripts\init_db.py
python scripts\demo_data.py
python run.py
```

访问：

```text
http://127.0.0.1:5000/
```

后台：

```text
http://127.0.0.1:5000/admin/login
```

默认管理员：

```text
admin / admin123456
```

## 十一、验收结果

已完成以下测试：

1. Python 语法检查通过。
2. 数据库初始化成功。
3. 演示数据导入成功。
4. 首页返回 200。
5. 分类页返回 200。
6. 标签页返回 200。
7. 搜索页返回 200。
8. 文章详情页返回 200。
9. 未登录访问后台返回 302。
10. 管理员登录成功。
11. 后台文章管理页返回 200。
12. 后台分类管理页返回 200。
13. 后台标签管理页返回 200。
14. 后台评论管理页返回 200。
15. 后台 AI 占位页返回 200。
16. 游客评论提交后进入待审核状态。
17. 后台新增文章流程可用。
18. 分类下存在文章时删除会被阻止。

## 十二、暂未实现功能

1. 真实 AI 接口。
2. AI 摘要生成。
3. AI 标签推荐。
4. AI 辅助写作。
5. Markdown 渲染。
6. 管理员修改密码。
7. 自动化测试套件。
8. 操作日志页面。

## 十三、V0.3 建议

下一版可以继续做：

1. 接入真实 AI 摘要生成。
2. 接入 AI 标签推荐。
3. 完善 AI 日志页面。
4. 增加 Markdown 渲染。
5. 增加管理员修改密码。
6. 增加 pytest 自动测试。
7. 增加文章草稿预览。
8. 增加操作日志。
