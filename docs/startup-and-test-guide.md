# 项目启动与测试说明

## 一、当前项目状态

当前项目为 V0.2，已经完成个人博客系统的非 AI 基础业务闭环。

当前可用功能包括：

1. 前台首页文章展示。
2. 文章详情页。
3. 分类浏览。
4. 标签浏览。
5. 关键词搜索。
6. 游客评论提交。
7. 评论审核后展示。
8. 管理员登录和退出。
9. 后台仪表盘。
10. 后台文章管理。
11. 后台分类管理。
12. 后台标签管理。
13. 后台评论管理。
14. AI 功能占位入口。

V0.2 暂不接入真实 AI 接口，不需要 API Key。

## 二、虚拟环境说明

本项目的虚拟环境名称是：

```text
.venv
```

虚拟环境只需要创建一次。如果项目根目录下已经存在 `.venv` 文件夹，就不需要重复创建，也不需要每次重新安装依赖。

只有在以下情况才需要重新安装依赖：

1. 第一次配置项目。
2. 删除了 `.venv`。
3. `requirements.txt` 发生变化。
4. 换了一台电脑或换了新的项目目录。

## 三、首次启动步骤

以下命令都在项目根目录执行：

```powershell
cd C:\Desktop\代码\personal-blog-system
```

### 1. 创建虚拟环境

仅第一次需要执行：

```powershell
python -m venv .venv
```

### 2. 激活虚拟环境

```powershell
.\.venv\Scripts\activate
```

激活后命令行前面通常会出现：

```text
(.venv)
```

### 3. 安装依赖

仅第一次或依赖变化时执行：

```powershell
pip install -r requirements.txt
```

### 4. 初始化数据库

```powershell
python scripts\init_db.py
```

该命令会创建数据表和默认管理员。

### 5. 插入演示数据

```powershell
python scripts\demo_data.py
```

该命令会创建演示分类、标签、文章和评论，方便直接验收。

### 6. 启动项目

```powershell
python run.py
```

正常启动后会看到：

```text
* Running on http://127.0.0.1:5000
```

访问：

```text
http://127.0.0.1:5000/
```

## 四、日常启动步骤

如果 `.venv` 已经存在，并且依赖和数据库都初始化过，以后只需要：

```powershell
cd C:\Desktop\代码\personal-blog-system
.\.venv\Scripts\activate
python run.py
```

然后访问：

```text
http://127.0.0.1:5000/
```

## 五、后台登录

后台入口：

```text
http://127.0.0.1:5000/admin/login
```

默认管理员：

```text
用户名：admin
密码：admin123456
```

该账号仅用于课程演示，正式使用前应修改默认密码。

## 六、停止项目

在运行 Flask 的终端里按：

```text
Ctrl + C
```

即可停止本地开发服务器。

## 七、基础自动测试

### 1. Python 语法检查

```powershell
.\.venv\Scripts\python.exe -m compileall app config.py run.py scripts
```

### 2. 首页和后台权限测试

```powershell
$env:PYTHONIOENCODING='utf-8'
.\.venv\Scripts\python.exe -c "from app import create_app; app=create_app(); c=app.test_client(); print(c.get('/').status_code); print(c.get('/admin/dashboard').status_code)"
```

预期结果：

```text
200
302
```

说明：

- `200` 表示首页可以访问。
- `302` 表示未登录访问后台会跳转到登录页。

## 八、手动验收流程

### 前台验收

1. 打开 `http://127.0.0.1:5000/`。
2. 确认首页有 Hero 区域和已发布文章卡片。
3. 点击文章，进入详情页。
4. 确认详情页显示标题、正文、分类、标签、浏览量和评论区。
5. 在详情页提交评论。
6. 确认页面提示“评论已提交，等待管理员审核”。
7. 访问 `/categories`，确认分类列表可用。
8. 点击分类，确认分类文章列表可用。
9. 访问 `/tags`，确认标签列表可用。
10. 点击标签，确认标签文章列表可用。
11. 使用搜索框搜索 `Flask`，确认搜索结果可用。

### 后台验收

1. 打开 `http://127.0.0.1:5000/admin/login`。
2. 使用 `admin / admin123456` 登录。
3. 确认进入后台仪表盘。
4. 查看文章、分类、标签、评论统计。
5. 进入文章管理，新增一篇文章。
6. 编辑文章状态为“已发布”。
7. 回到前台，确认文章可见。
8. 进入分类管理，新增和编辑分类。
9. 尝试删除已有文章的分类，确认系统阻止删除。
10. 进入标签管理，新增、编辑和删除标签。
11. 进入评论管理，审核刚才提交的评论。
12. 回到文章详情页，确认审核通过的评论显示。
13. 进入 AI 占位页面，确认只显示“后续版本开放”。

## 九、常见问题

### 1. 提示缺少 Flask 或 flask_login

说明没有激活虚拟环境，或者依赖没有安装。

```powershell
.\.venv\Scripts\activate
pip install -r requirements.txt
```

### 2. 数据库里没有文章

请执行：

```powershell
python scripts\init_db.py
python scripts\demo_data.py
```

### 3. 端口 5000 被占用

可以临时换端口启动：

```powershell
.\.venv\Scripts\python.exe -c "from app import create_app; app = create_app(); app.run(debug=True, port=5001)"
```

然后访问：

```text
http://127.0.0.1:5001/
```

### 4. 激活虚拟环境失败

如果 PowerShell 阻止脚本执行，可以临时执行：

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

然后重新执行：

```powershell
.\.venv\Scripts\activate
```

## 十、后续说明

V0.3 可以继续接入 AI 摘要、AI 标签推荐、AI 辅助写作和 AI 操作日志页面。V0.2 已经为这些能力保留了 `app/ai/` 模块和后台入口。
