# 项目启动与测试说明

## 一、当前版本

当前项目为 V0.3：多用户知识专栏博客系统。

核心定位：

```text
每个用户都可以创建自己的专栏、发布自己的文章、阅读和交流别人知识内容。
```

系统不是单人博客，也不是知乎式问答社区。

## 二、虚拟环境

虚拟环境名称：

```text
.venv
```

如果 `.venv` 已经存在，日常启动不需要重新创建，也不需要每次重新安装依赖。

## 三、首次启动

```powershell
cd C:\Desktop\代码\personal-blog-system
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python scripts\init_db.py --reset
python scripts\demo_data.py
python run.py
```

访问：

```text
http://127.0.0.1:5000/
```

## 四、日常启动

```powershell
cd C:\Desktop\代码\personal-blog-system
.\.venv\Scripts\activate
python run.py
```

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

## 六、基础自动测试

语法检查：

```powershell
.\.venv\Scripts\python.exe -m compileall app config.py run.py scripts
```

路由快速测试：

```powershell
$env:PYTHONIOENCODING='utf-8'
.\.venv\Scripts\python.exe -c "from app import create_app; app=create_app(); c=app.test_client(); print(c.get('/').status_code); print(c.get('/columns').status_code); print(c.get('/admin/dashboard').status_code)"
```

预期结果：

```text
200
200
302
```

## 七、手动验收

游客：

1. 访问首页。
2. 浏览文章、分类、标签和专栏。
3. 进入作者主页。
4. 使用搜索框搜索文章。
5. 未登录时尝试点赞、收藏或评论，会跳转登录。

普通用户：

1. 使用 `alice / user123456` 登录。
2. 进入个人中心。
3. 创建专栏。
4. 发布文章。
5. 编辑或删除自己的文章。
6. 点赞、收藏、评论其他用户文章。
7. 在个人中心查看互动记录。

管理员：

1. 使用 `admin / admin123456` 登录后台。
2. 查看仪表盘。
3. 管理用户、文章、专栏、分类、标签和评论。
4. 使用普通用户登录后访问后台，确认不能进入。

## 八、常见问题

### 1. 数据库结构不匹配

V0.3 修改了数据库结构。如果页面报数据库字段不存在，请重建演示库：

```powershell
python scripts\init_db.py --reset
python scripts\demo_data.py
```

### 2. 缺少依赖

```powershell
.\.venv\Scripts\activate
pip install -r requirements.txt
```

### 3. 端口 5000 被占用

```powershell
.\.venv\Scripts\python.exe -c "from app import create_app; app = create_app(); app.run(debug=True, port=5001)"
```

然后访问：

```text
http://127.0.0.1:5001/
```
