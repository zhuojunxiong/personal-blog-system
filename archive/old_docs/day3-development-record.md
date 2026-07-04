# 第三天开发记录：V0.3 多用户知识专栏平台

## 一、定位纠偏

V0.3 将系统从“管理员写、游客看”的个人博客，升级为“多用户知识专栏博客系统”。

新的定位是：

```text
每个用户都能建立自己的专栏、写自己的博客、阅读和交流别人知识内容。
```

系统不是知乎式问答社区，也不是商业化内容平台。文章和专栏是中心，互动只是增强。

## 二、本次完成的核心功能

1. 普通用户注册、登录、退出。
2. 用户个人资料。
3. 作者主页。
4. 用户个人中心。
5. 用户创建和管理自己的专栏。
6. 用户发布、编辑、删除自己的文章。
7. 文章归属作者和专栏。
8. 文章详情页显示作者和专栏。
9. 登录用户点赞文章。
10. 登录用户收藏文章。
11. 登录用户评论文章。
12. 用户个人中心展示收藏、点赞和评论记录。
13. 管理员管理用户。
14. 管理员管理全站专栏。
15. 后台只允许管理员访问。
16. 首页展示推荐专栏和活跃作者。
17. 搜索支持作者和标签。
18. AI 功能继续只做占位。

## 三、数据库结构变化

### User

新增或完善：

- `email`
- `bio`
- `avatar`
- `role`
- `status`

用户角色包括：

- `user`
- `admin`

### BlogColumn

新增专栏模型：

- `id`
- `user_id`
- `name`
- `description`
- `status`
- `created_at`
- `updated_at`

### Article

新增或完善：

- `user_id`
- `column_id`
- `like_count`
- `favorite_count`

### Comment

新增：

- `user_id`

评论仍然需要审核后才在前台显示。

### Like

新增点赞模型，同一用户不能重复点赞同一篇文章。

### Favorite

新增收藏模型，同一用户不能重复收藏同一篇文章。

## 四、新增和修改的主要文件

新增：

- `app/user/`
- `app/column/`
- `app/admin/decorators.py`
- `app/templates/user/`
- `app/templates/public/columns.html`
- `app/templates/public/column_detail.html`
- `app/templates/public/user_profile.html`
- `app/templates/admin/users/index.html`
- `app/templates/admin/columns/index.html`
- `app/templates/errors/403.html`

修改：

- `app/models.py`
- `app/__init__.py`
- `app/auth/routes.py`
- `app/public/routes.py`
- `app/article/routes.py`
- `app/comment/routes.py`
- `app/static/css/main.css`
- `scripts/init_db.py`
- `scripts/demo_data.py`
- `README.md`
- `docs/startup-and-test-guide.md`

## 五、测试账号

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

## 六、验收结果

已完成验证：

1. 语法检查通过。
2. 数据库 reset 初始化成功。
3. V0.3 演示数据导入成功。
4. 游客访问首页、文章、分类、标签、专栏、作者主页均返回 200。
5. 普通用户登录成功。
6. 普通用户可以进入个人中心。
7. 普通用户可以创建专栏。
8. 普通用户可以发布文章。
9. 普通用户可以点赞、收藏、评论文章。
10. 普通用户访问后台会被拒绝或重定向。
11. 管理员登录成功。
12. 管理员可以访问后台仪表盘、用户管理、专栏管理、文章管理和评论管理。

## 七、暂未实现

1. 真实 AI 接口。
2. Markdown 渲染。
3. 用户修改密码。
4. 自动化测试套件。
5. 复杂推荐算法。
6. 私信、关注、热榜、付费专栏。

## 八、下一步 V0.4

建议继续做：

1. Markdown 编辑和渲染。
2. AI 摘要和标签推荐。
3. 用户修改密码。
4. 自动化测试。
5. 操作日志。
6. 文章草稿预览。
