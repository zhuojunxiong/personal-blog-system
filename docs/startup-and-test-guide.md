# 项目启动与 DeepSeek AI 接入完整教程

当前版本：**V0.5.1** — 多用户知识专栏博客系统「稷下」，已集成 AI 智能搜索。

---

## 一、环境准备

### Windows

1. **安装 Python 3.10+**
   - 前往 https://www.python.org/downloads/ 下载安装包
   - ✅ 勾选 "Add Python to PATH"
   - 验证：`python --version`

2. **安装 Git**
   - 前往 https://git-scm.com/download/win 下载安装
   - 验证：`git --version`

3. **创建虚拟环境**
   ```powershell
   cd "你的项目路径\personal-blog-system"
   python -m venv .venv
   ```

### Mac

1. **安装 Python 3.10+**
   ```bash
   brew install python@3.12
   ```
   验证：`python3 --version`

2. **创建虚拟环境**
   ```bash
   cd "你的项目路径/personal-blog-system"
   python3 -m venv .venv
   ```

---

## 二、安装依赖

```bash
# Windows
.venv\Scripts\python -m pip install -r requirements.txt

# Mac
.venv/bin/python -m pip install -r requirements.txt
```

---

## 三、🔑 接入最强 DeepSeek API（必读）

### 3.1 获取 API Key

1. 打开 [DeepSeek 开放平台](https://platform.deepseek.com)
2. 注册 / 登录账号
3. 进入 **API Keys** 页面 → 点击「创建 API Key」
4. 复制 Key（格式：`sk-xxxxxxxxxxxxxxxx`）

> ⚠️ **安全警告**：API Key 不要写进代码、README、或截图分享。任何人拿到你的 Key 都可以以你的名义调用 API 并产生费用。

### 3.2 模型选择指南

| 模型 | 特点 | 适用场景 |
|------|------|----------|
| **`deepseek-chat`**（推荐） | DeepSeek-V3 最新旗舰，综合能力最强，128K 上下文 | 摘要、润色、问答、搜索 |
| **`deepseek-reasoner`** | DeepSeek-R1 推理模型，逻辑推理极强，速度较慢 | 复杂逻辑分析、代码审查 |
| `deepseek-v4-flash` | 速度快、成本极低 | 标签推荐等简单任务 |

**本项目的 AI 功能**自动根据场景选择最佳参数，你只需配置模型名称即可。

### 3.3 Windows 启动（推荐方式）

**方法一：终端环境变量（推荐）**

```powershell
# PowerShell
$env:AI_API_KEY="sk-你的APIKey"
$env:AI_MODEL="deepseek-chat"
.venv\Scripts\python run.py
```

**方法二：创建 `.env` 文件（一次配置，永久生效）**

在 `personal-blog-system/` 目录下新建 `.env` 文件：

```bash
# .env 文件内容
AI_API_KEY=sk-你的APIKey
AI_MODEL=deepseek-chat
AI_BASE_URL=https://api.deepseek.com
AI_MAX_TOKENS=2000
AI_TIMEOUT=30
```

然后安装 `python-dotenv` 并修改 `run.py`（见下方代码）：

```powershell
.venv\Scripts\pip install python-dotenv
```

修改 `run.py` 为：

```python
from dotenv import load_dotenv
load_dotenv()  # 自动读取 .env 文件中的环境变量

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
```

之后直接启动即可：

```powershell
.venv\Scripts\python run.py
```

### 3.4 Mac 启动

**方法一：终端环境变量**

```bash
export AI_API_KEY="sk-你的APIKey"
export AI_MODEL="deepseek-chat"
.venv/bin/python run.py
```

**方法二：`.env` 文件**（同 Windows 方法二，`.env` 文件内容相同）

```bash
.venv/bin/pip install python-dotenv
.venv/bin/python run.py
```

### 3.5 使用自定义 API 中转（高级）

如果你在国内网络环境下需要代理访问，或使用兼容接口：

```bash
# Windows PowerShell
$env:AI_BASE_URL="https://你的中转地址"
$env:AI_MODEL="deepseek-v4-pro[1m]"

# Mac
export AI_BASE_URL="https://你的中转地址"
export AI_MODEL="deepseek-v4-pro[1m]"
```

### 3.6 验证 AI 是否接入成功

启动后，用任意账号登录 → 进入「个人中心」→ 点击「写文章」→ 右侧 AI 面板：

- 输入一段正文，点击「**生成摘要**」→ 如果几秒后返回结构化摘要，说明 AI 接入成功
- 如果提示「AI 接口未配置」，检查 `AI_API_KEY` 是否设置正确

管理员可在后台 `/admin/ai` 查看 AI 接口状态。

---

## 四、初始化数据库

### 首次使用

```bash
# Windows
.venv\Scripts\python scripts\init_db.py
.venv\Scripts\python scripts\demo_data.py

# Mac
.venv/bin/python scripts/init_db.py
.venv/bin/python scripts/demo_data.py
```

### 重新构建（清空旧数据）

```bash
# Windows
.venv\Scripts\python scripts\init_db.py --reset
.venv\Scripts\python scripts\demo_data.py

# Mac
.venv/bin/python scripts/init_db.py --reset
.venv/bin/python scripts/demo_data.py
```

> `--reset` 会删除所有旧数据，仅用于开发演示。

---

## 五、访问系统

浏览器打开 **http://127.0.0.1:5000/**

### 测试账号

| 角色 | 用户名 | 密码 | 身份 |
|------|--------|------|------|
| 管理员 | `admin` | `admin123456` | 系统管理员 |
| 普通用户 | `alice` | `user123456` | 全栈开发者 — 林知夏 |
| 普通用户 | `bob` | `user123456` | 算法工程师 — 周远航 |
| 普通用户 | `carol` | `user123456` | 前端设计师 — 陈青禾 |
| 普通用户 | `zhaomingyuan` | `user123456` | 金融分析师 — 赵明远 |
| 普通用户 | `suxiaoyu` | `user123456` | 内科医生 — 苏晓雨 |
| 普通用户 | `wangjianyu` | `user123456` | 建筑工程师 — 王建宇 |
| 普通用户 | `liuyihan` | `user123456` | UI/UX 设计师 — 刘艺涵 |
| 普通用户 | `sunjiahe` | `user123456` | 高中语文教师 — 孙嘉禾 |
| 普通用户 | `masiyuan` | `user123456` | 知识产权律师 — 马思远 |
| 普通用户 | `wuanran` | `user123456` | 心理咨询师 — 吴安然 |
| 普通用户 | `xuqingfeng` | `user123456` | 职业厨师 — 许清风 |
| 普通用户 | `zhengyiming` | `user123456` | 连续创业者 — 郑一鸣 |
| 普通用户 | `huangyutong` | `user123456` | 产品经理 — 黄雨桐 |

> 所有普通用户密码相同：`user123456`

---

## 六、AI 功能一览

| 功能 | 说明 | 使用位置 |
|------|------|----------|
| 🔍 **AI 智能搜索** | 理解自然语言搜索意图，即使搜索词不精确也能找到相关文章 | 首页 / 搜索页 |
| 📝 **生成摘要** | 分析文章内容，生成结构化摘要（200 字以内，含要点列表） | 写文章页 AI 面板 |
| 🏷️ **推荐标签** | 自动推荐 3-8 个精准中文标签 | 写文章页 AI 面板 |
| ✨ **润色正文** | 逐段润色，修正语病、调整结构、解释术语 | 写文章页 AI 面板 |
| 📋 **提取大纲** | 分析文章结构，提取或归纳章节标题 | 写文章页 AI 面板 |
| ✏️ **标题建议** | 生成 5 个候选标题（3 务实型 + 2 吸引型） | 写文章页 AI 面板 |
| 💬 **文章问答** | 基于文章内容回答写作问题，支持改进建议、结构分析 | 写文章页 AI 面板问答框 |

### AI 智能搜索使用示例

试试这些搜索词，体验 AI 理解意图的能力：

| 你输入 | AI 理解 | 应该找到 |
|--------|---------|----------|
| `想学 Flask 部署怎么弄` | 你想学习如何将 Flask 应用部署到服务器上… | Flask 部署、Nginx、服务器相关文章 |
| `有没有关于数据库的经验` | 你在寻找数据库设计方面的经验分享… | SQLite 模型设计、数据库实践文章 |
| `最近总是焦虑怎么办` | 你想了解如何管理和缓解焦虑情绪… | 心理咨询师关于焦虑管理的文章 |
| `红烧肉怎么做` | 你想了解红烧肉的做法和相关美食知识… | 美食文化、烹饪技巧文章 |
| `那个设计的东西` | 你在寻找 UI/交互设计相关的内容… | 设计思维、用户体验文章 |

---

## 七、手动验收流程

### 游客体验
1. 访问首页 → 看到落地页和 AI 搜索框
2. 使用搜索框搜索 → AI 理解搜索意图并返回结果
3. 浏览文章、分类、标签、专栏
4. 未登录时点赞/收藏/评论 → 跳转登录页

### 普通用户（AI 功能测试）
1. 用 `alice / user123456` 登录
2. 首页搜索框输入"想学部署" → 验证 AI 智能搜索
3. 点击「写文章」，输入标题和正文（至少 200 字）
4. 依次点击 AI 按钮：生成摘要 → 推荐标签 → 润色正文 → 提取大纲 → 标题建议
5. 在问答框输入"这篇文章可以如何改进？"并发送
6. 发布文章后，切换到其他账号登录，点赞、收藏、评论
7. 查看个人中心的互动记录

### 管理员
1. 用 `admin / admin123456` 登录后台 `/admin/login`
2. 查看仪表盘数据
3. 管理用户、文章、专栏、分类、标签、评论
4. 查看 AI 接口状态 `/admin/ai`
5. 用普通用户账号访问 `/admin` → 被 403 拒绝

---

## 八、完整环境变量参考

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `AI_API_KEY` | （空） | DeepSeek API Key，不设置则 AI 功能不可用 |
| `AI_MODEL` | `deepseek-chat` | 模型名称 |
| `AI_BASE_URL` | `https://api.deepseek.com` | API 地址，可改为中转 |
| `AI_MAX_TOKENS` | `2000` | 默认最大输出 token |
| `AI_TIMEOUT` | `30` | 请求超时（秒） |
| `AI_ENABLED` | `1` | 设为 `0` 关闭所有 AI 功能 |
| `SECRET_KEY` | （自动生成） | Flask 密钥 |
| `WTF_CSRF_SECRET_KEY` | （自动生成） | CSRF 保护密钥 |

---

## 九、常见问题

### 服务关不掉
运行 `run.py` 的终端按 `Ctrl + C`。

### 页面提示「AI 接口未配置」
当前终端没有设置 `AI_API_KEY`。在**同一个终端**中设置后再启动：
```bash
# Windows PowerShell
$env:AI_API_KEY="sk-你的Key"

# Mac
export AI_API_KEY="sk-你的Key"
```

### AI 返回内容质量不高
1. 确保使用 **`deepseek-chat`**（最强模型），不是 v4-flash
2. 正文至少 200 字，AI 需要足够上下文
3. 搜索时描述尽量具体，如"怎么部署 Flask 到服务器"比"部署"更好

### AI 接口返回错误
- API Key 写错 → 检查是否有多余空格
- DeepSeek 账号余额不足 → 去 platform.deepseek.com 充值
- 网络不通 → 检查是否需要代理，或用中转地址

### 端口 5000 被占用
```bash
# Windows
.venv\Scripts\python -c "from app import create_app; app=create_app(); app.run(debug=True, port=5001)"

# Mac
.venv/bin/python -c "from app import create_app; app=create_app(); app.run(debug=True, port=5001)"
```
然后访问 `http://127.0.0.1:5001/`

### 缺少依赖
```bash
# Windows
.venv\Scripts\pip install -r requirements.txt

# Mac
.venv/bin/pip install -r requirements.txt
```

### 数据库表不存在
```bash
# Windows
.venv\Scripts\python scripts\init_db.py --reset
.venv\Scripts\python scripts\demo_data.py

# Mac
.venv/bin/python scripts/init_db.py --reset
.venv/bin/python scripts/demo_data.py
```

---

## 十、⚡ 一键启动（Windows）

项目根目录下已提供 `启动项目.bat`，双击即可：

1. **首次使用**：编辑 `.env` 文件，填入你的 API Key
2. 双击 `启动项目.bat`
3. 脚本自动完成：安装依赖 → 初始化数据库 → 写入演示数据 → 启动服务器
4. 浏览器打开 `http://127.0.0.1:5000/`

---

## 十一、快速启动一览

```bash
# === 首次使用（Windows PowerShell）===
cd "项目路径\personal-blog-system"
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python scripts\init_db.py
.venv\Scripts\python scripts\demo_data.py
$env:AI_API_KEY="sk-你的APIKey"
$env:AI_MODEL="deepseek-chat"
.venv\Scripts\python run.py

# === 首次使用（Mac）===
cd "项目路径/personal-blog-system"
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python scripts/init_db.py
.venv/bin/python scripts/demo_data.py
export AI_API_KEY="sk-你的APIKey"
export AI_MODEL="deepseek-chat"
.venv/bin/python run.py

# 浏览器打开 http://127.0.0.1:5000/
```
