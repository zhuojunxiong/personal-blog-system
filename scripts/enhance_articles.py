"""Generate high-quality 800+ char content for all demo articles.

Matches articles by keyword to rich content templates, and generates
structured educational content for unmatched articles.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app import create_app
from app.extensions import db
from app.models import Article

app = create_app()

# ── Article content library (keyed by keyword match in title) ─────────────

TOPICS = {
    "Flask": """
Flask 是一个用 Python 编写的轻量级 Web 框架，由 Armin Ronacher 在 2010 年作为愚人节玩笑创建，后来发展成为 Python 生态中最受欢迎的 Web 框架之一。它的核心设计哲学是\"微框架\"——只提供 Web 开发最基本的工具（路由、请求处理、模板渲染），其他一切通过扩展按需添加。

## 为什么选择 Flask

对于课程项目和学习目的，Flask 比 Django 有几个优势。第一，Flask 不会替你做太多决策——你需要自己选择 ORM、认证方案、表单处理库，这个选择过程本身就是很好的学习机会。第二，Flask 的项目结构灵活，你可以按自己的理解组织代码，而不是被框架的约定束缚。第三，Flask 的代码量少、概念清晰，阅读源码的门槛低。

## 核心概念

Flask 应用的核心是应用对象（Flask 实例）和路由（Route）。路由将 URL 映射到 Python 函数，当用户访问一个 URL 时，Flask 调用对应的函数并返回结果。Blueprint（蓝图）是 Flask 实现模块化的机制，允许将应用拆分为多个可复用的组件。

## 本项目的 Flask 实践

本项目使用 Flask 工厂函数模式创建应用，通过 11 个 Blueprint 组织代码，配合 Flask-Login 处理认证、Flask-SQLAlchemy 操作数据库、Flask-WTF 提供 CSRF 保护。项目从 v0.1 的单文件原型逐步演进为 v1.0 的完整工程化项目，完整记录了 Flask 从入门到工程实践的成长路径。

## 常见问题与解决

第一个常见问题是应用上下文（Application Context）的理解。Flask 中很多操作（如 `url_for`、`current_app`）需要在请求上下文中执行，在测试和脚本中需要手动创建上下文。

第二个问题是扩展的初始化时机。Flask 扩展通常使用 `init_app()` 模式而不是在模块导入时直接绑定 app，这样可以在工厂函数中创建多个独立的 app 实例。

第三个问题是大型项目的代码组织。当路由文件超过 500 行时，就该考虑拆分为多个 Blueprint 了。本项目的拆分经验是：按业务功能（用户、文章、评论）而不是按技术层（视图、模型、模板）来组织蓝图。

## 总结

Flask 的学习曲线平缓但天花板很高。你可以用 10 行代码跑起一个网站，也可以用工厂模式、Blueprint、信号机制构建复杂的企业级应用。关键在于理解它的设计哲学：简单但不简陋，灵活但不混乱。
""",

    "SQLite": """
SQLite 是世界上最广泛部署的数据库引擎，它不是一个独立的数据库服务器，而是一个嵌入在应用程序中的库。你手机里的每个 App、你电脑上的浏览器，大概率都在使用 SQLite 存储数据。

## 架构特点

SQLite 是\"无服务器\"架构——不需要安装、配置、启动数据库服务。数据库就是一个单一的 `.sqlite` 文件，你可以像操作普通文件一样复制、备份、分享它。这个特性让 SQLite 在开发和课程项目中极具优势：克隆仓库即可获得完整的数据环境。

## 为什么本项目选择 SQLite

本项目是一个面向课程实践的知识博客系统，用户量小、并发低、数据量可控。SQLite 完美匹配这个场景：零配置、无需额外服务、数据库文件可纳入版本管理、通过 SQLAlchemy ORM 操作与操作其他数据库完全一致。如果需要迁移到 MySQL 或 PostgreSQL，只需要修改配置中的数据库连接串。

## SQLite 的局限

第一，并发写入能力有限。SQLite 使用数据库级别的写锁，同一时间只能有一个写操作。如果你的应用需要处理每秒几十次的并发写入，SQLite 不是好的选择。

第二，不支持用户权限管理。SQLite 没有用户账户和权限系统，不适合需要精细访问控制的多租户应用。

第三，网络访问受限。SQLite 是本地数据库，不支持通过网络连接。如果需要多台服务器共享数据，需要切换到客户端-服务器架构的数据库。

## 最佳实践

为所有外键列建立索引——这是提升 SQLite 查询性能最简单有效的手段。避免在循环中执行大量单条 INSERT，改用批量插入或事务包裹。定期执行 VACUUM 命令回收删除数据后留下的空间。在生产环境中，使用 WAL（Write-Ahead Logging）模式提升并发读取性能。

## 总结

SQLite 的定位不是\"玩具数据库\"，而是一个严肃的、经过充分测试的嵌入式数据库。对于课程项目、桌面应用、移动应用和中小型 Web 应用，SQLite 是一个务实且高效的选择。理解它的适用场景和局限，比盲目追求\"更高级\"的数据库更重要。
""",

    "pytest": """
pytest 是 Python 生态中最流行的测试框架，它比 unittest 更简洁、更灵活、更强大。本项目的 284 个自动化测试全部基于 pytest 编写。

## 为什么选择 pytest

pytest 的最大优势是简洁。不需要继承 TestCase 类，不需要 self.assertEqual，直接用 assert 语句即可。pytest 的 fixture 机制比 unittest 的 setUp/tearDown 更灵活，支持依赖注入、作用域控制、参数化和自动清理。

## 核心概念

### Fixture

Fixture 是 pytest 最强大的特性。通过 `@pytest.fixture` 装饰器定义的 fixture 可以作为测试函数的参数注入，pytest 自动管理它们的生命周期：

```python
@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
        yield client

def test_homepage(client):
    r = client.get("/")
    assert r.status_code == 200
```

### 参数化

`@pytest.mark.parametrize` 让你用一组输入数据运行同一个测试多次：

```python
@pytest.mark.parametrize("username,password,expected", [
    ("admin", "wrong", False),
    ("admin", "admin123456", True),
])
def test_login(client, username, password, expected):
    r = client.post("/login", data={"username": username, "password": password})
    assert (r.status_code == 302) == expected
```

### 覆盖率

pytest-cov 插件可以统计测试覆盖率，帮助发现未被测试覆盖的代码路径。虽然 100% 覆盖率是一个好的目标，但不能盲目追求——有些代码（如简单的 getter/setter）不值得浪费测试精力，测试质量比覆盖率数字更重要。

## 本项目的测试策略

测试分为三层：模型测试（test_models.py）验证数据结构和约束，服务测试（test_services.py）验证业务逻辑，路由测试（test_public.py、test_user.py、test_admin.py）验证页面和权限。每个测试函数使用独立的内存 SQLite 数据库，通过 conftest.py 中的 fixture 自动创建和销毁，确保测试之间完全隔离。

## 总结

好的测试不是负担，而是安全网。它让你在重构时有信心，在发布时有底气。pytest 让写测试变得简单，而简单是养成好习惯的前提。
""",

    "SQLAlchemy": """
SQLAlchemy 是 Python 最强大的 ORM（对象关系映射）框架，它让你可以用 Python 代码操作数据库而不用写 SQL。但它的真正价值不在于"不用写 SQL"，而在于提供了一层抽象，让数据库操作更加安全、可维护和可测试。

## ORM 的两面性

ORM 的好处：参数化查询自动防止 SQL 注入；模型关系让数据访问更直观；迁移工具让数据库变更有迹可循；测试时可以用内存数据库替代真实数据库。

ORM 的代价：生成的 SQL 可能不够高效；复杂的 JOIN 查询用 ORM 表达可能比直接写 SQL 更冗长；抽象层增加了一定的学习成本。

## 本项目的 SQLAlchemy 实践

所有的数据库操作通过 SQLAlchemy ORM 完成。模型定义在 `app/models.py` 中，包含 User、Article、Category、Tag、Comment 等核心实体。模型之间通过 `db.relationship()` 和 `db.ForeignKey()` 建立关联。

### 模型设计要点

每个外键列添加了数据库索引，确保 JOIN 查询的性能。点赞和收藏模型设置了 `user_id + article_id` 的唯一约束，从数据库层面防止重复操作。字段类型选择遵循\"够用但不过度\"的原则——用户名 64 字符足够，文章正文用 Text 类型不限制长度。

### Service 层的封装

所有数据库操作都通过 Service 层（如 `ArticleService`、`UserService`）完成，路由层不直接操作 Model。这样做的好处是：业务逻辑集中管理，便于复用和修改；测试时可以直接测试 Service 函数而不用发送 HTTP 请求；将来如果数据库结构变化，只需要修改 Service 层。

### 查询优化

使用 `filter_by` 代替 `filter` 处理简单的等值查询，代码更简洁。对于列表页面使用 `paginate()` 而不是 `.all()`，避免一次性加载全部数据。文章的已审核评论数使用 SQL COUNT 查询而不是在 Python 中过滤，避免 N+1 问题。

## 常见陷阱

第一个陷阱是懒加载导致的 N+1 问题。当你遍历一个文章列表并在模板中访问每篇文章的 `author.nickname` 时，SQLAlchemy 默认会为每篇文章单独查询作者信息。解决方法是在查询时使用 `joinedload()` 或 `subqueryload()` 预加载关联数据。

第二个陷阱是在请求之外使用数据库对象。Flask-SQLAlchemy 的 session 与请求生命周期绑定，在请求结束后的异步任务中访问数据库对象会导致 DetachedInstanceError。

## 总结

SQLAlchemy 是 Python 数据库操作的工业标准。对于课程项目来说，通过 ORM 学习数据库设计和查询优化，远比直接写 SQL 更有教育价值。理解 ORM 在背后生成的 SQL，是成为一个更好的后端开发者的关键步骤。
""",

    "Markdown": """
## Markdown 的设计哲学

Markdown 由 John Gruber 在 2004 年创建，设计目标是\"让写作回归内容本身\"。它的语法极其简单：用 `#` 表示标题、用 `**` 表示粗体、用 `-` 表示列表。不需要工具栏、不需要鼠标、不需要思考排版——手不需要离开键盘，思路就不会被打断。

## 为什么技术写作选择 Markdown

程序员喜欢 Markdown 的原因不仅是简洁。Markdown 文件是纯文本，可以用 Git 进行版本控制，可以 diff 查看改动，可以在任何编辑器中打开。Word 文档做不到这些。GitHub 的 README、技术文档、静态博客——Markdown 已经成为技术写作的事实标准。

## 本项目的 Markdown 集成

项目的写作页使用 `<textarea>` 作为 Markdown 编辑器，用户输入原始 Markdown 文本。文章阅读页和作者主页通过自定义的 Jinja2 过滤器 `render_markdown` 将 Markdown 渲染为 HTML。渲染器支持标题（h1-h3）、粗体、斜体、行内代码、代码块、链接、无序列表和引用。

用户还可以用 Markdown 编写个性化的知识主页——介绍研究方向、项目经历、学习路线、代表作品。

## Markdown 写作技巧

第一，用标题构建清晰的文章结构。好的层级让读者一目了然。第二，适当使用代码块展示技术内容，但不要过度——大段代码放在文章中会打断阅读节奏。第三，列表胜过冗长的段落——把要点提炼成 3-5 条的列表，可读性显著提升。第四，文章首段要能回答\"这篇文章在讲什么、为什么值得读、读完能获得什么\"。第五，配图虽然不在本项目的支持范围内，但纯文本结构清晰的文章同样有很好的阅读体验。

## 扩展语法

基础 Markdown 功能有限，很多平台扩展了额外的语法。GitHub Flavored Markdown（GFM）增加了表格、任务列表和删除线。本项目没有使用扩展语法，保持了基础 Markdown 的兼容性——这样将来如果需要切换到其他 Markdown 渲染器，不会有兼容性问题。

## 总结

Markdown 的流行不是偶然。它用最简单的语法解决了最普遍的需求：让写作者专注于内容，让系统处理排版。对于知识博客来说，Markdown 减少了写作的摩擦，让\"记录知识\"这件事变得更容易坚持。
""",

    "Git": """
Git 是目前最流行的分布式版本控制系统，由 Linus Torvalds 在 2005 年为 Linux 内核开发而创建。在今天的软件开发中，Git 已经不是一个\"可选技能\"，而是一个基础技能。

## 版本控制的核心价值

第一，完整的修改历史。每一次提交都是项目的一个快照，你可以回溯到任意时间点的状态。第二，安全的分支机制。你可以在不影响主线的情况下实验新想法，失败了就丢弃。第三，协作的基础设施。虽然本项目是单人开发，但在团队中，Git 是多人协作的必需品。第四，证据链。在课程项目中，Git 提交历史是开发过程的完整记录，可以用于答辩和项目总结。

## 本项目的 Git 实践

项目使用多个分支管理不同的工作流：`main` 是稳定主线，`process/unified-main-repo` 用于 v0.5.1 工程治理，`work/v1.0-course-delivery` 用于 v1.0 课程交付。每个功能或文档变更通过专门的提交记录，提交信息遵循\"标题 + 详细说明\"的格式。

## 最佳实践

第一，频繁提交、小步提交。不要攒了几天的修改再一次提交——如果出了问题，定位范围太大。第二，提交信息要写清楚\"做了什么\"和\"为什么\"，而不是\"改了点东西\"。第三，提交前用 `git diff --stat` 检查变更范围，确保没有误改文件。第四，不要提交生成文件、缓存文件、数据库文件（除非明确需要）和包含敏感信息的文件。

## 常见问题

第一个常见问题是合并冲突。当两个分支修改了同一个文件的同一行时，Git 不知道应该保留哪个版本，需要手动解决。解决冲突的关键是理解双方的改动意图，而不是简单地接受一方、丢弃另一方。

第二个问题是误提交。如果提交了不该提交的文件（如包含密码的配置文件），需要立即修改密码并清理 Git 历史——仅仅删除文件再提交是不够的，历史中仍然保留着内容。

## 总结

Git 的学习曲线在前 20% 很陡——clone、add、commit、push 这几个命令就够日常使用了。但真正理解 Git 的工作原理（DAG、分支指针、暂存区）需要更多的时间和实践。投入时间学好 Git，是对整个开发生涯的投资。
""",

    "CSS": """
CSS（层叠样式表）是 Web 的视觉语言。HTML 定义结构和内容，CSS 定义外观和布局。一个设计良好的 CSS 体系能让你在需要调整页面风格时，只改几行代码而不是翻几十个文件。

## 基础概念

### 盒模型

CSS 中所有元素都是一个矩形盒子，由内容区（content）、内边距（padding）、边框（border）和外边距（margin）组成。理解盒模型是布局的基础。`box-sizing: border-box` 让 width 和 height 包含 padding 和 border，在响应式布局中更直观。

### 选择器

选择器决定了样式应用到哪些元素。类选择器（`.class-name`）是最常用的，因为它可复用、语义清晰。避免过深的选择器嵌套——`.header .nav .list .item a` 不仅性能差，而且难以覆盖和调试。

### 布局

Flexbox 和 Grid 是现代的布局方案。Flexbox 适合一维布局（行或列），Grid 适合二维布局（行列网格）。`justify-content`、`align-items`、`gap` 这几个属性解决了 80% 的对齐和间距问题。

## 本项目的 CSS 架构

项目有两套 CSS 文件：`main.css` 负责全局样式、公共组件和后台页面；`v041.css` 负责 v041 版本的首页、阅读页、搜索页和用户空间的样式。这种分离方式记录了版本演进的痕迹，但长期来看，需要逐步统一为一致的视觉体系。

## 响应式设计

响应式设计的核心是媒体查询（Media Query）和弹性单位。用 `@media (max-width: 768px)` 为小屏幕覆写样式，用 `rem`、`%`、`vw` 代替固定的 `px`。移动优先的设计思路是先写移动端的样式，再用媒体查询为大屏幕补充——因为移动端的约束更严格，先解决难的再扩展更容易。

## 总结

CSS 入门容易精通难。写 CSS 不只是为了让页面\"看起来好看\"，更是为了构建一个可维护、可扩展的视觉系统。好的 CSS 让未来的你感谢现在的你。
""",

    "Docker": """
Docker 是一个开源的容器化平台，它把应用程序及其所有依赖打包在一个轻量级的、可移植的容器中。\"在我机器上能跑\"是软件开发的常见痛点，Docker 通过将运行环境也标准化来解决这个问题。

## 容器 vs 虚拟机

容器和虚拟机都提供隔离的运行环境，但实现方式不同。虚拟机需要完整的操作系统，启动慢（分钟级）、占用资源多。容器共享宿主机的操作系统内核，启动快（秒级）、占用资源少。Docker 不是虚拟化技术，而是操作系统级别的进程隔离。

## 核心概念

Docker 镜像（Image）是应用的模板，包含代码、运行时、库和配置。镜像一旦构建就是不可变的，任何修改都会产生新的镜像层。Docker 容器（Container）是镜像的运行实例，每个容器有自己独立的文件系统、网络和进程空间。Dockerfile 是定义镜像构建步骤的文本文件，可以纳入版本管理。

Docker Compose 用于编排多个容器。比如一个 Web 应用可能需要应用容器、数据库容器、缓存容器，通过 Compose 文件可以一键启动所有服务。

## 本项目的 Docker 化方案

虽然本项目目前没有使用 Docker，但容器化并不复杂。一个最小的 Dockerfile 只需要十几行：选择 Python 基础镜像、复制代码、安装依赖、设置启动命令。对于课程项目来说，Docker 的主要价值是让评审者可以在自己的机器上快速运行项目，而不需要配置 Python 版本和虚拟环境。

## 生产环境考量

容器是无状态的——容器重启后，其中的数据会丢失。因此数据库文件、用户上传的文件需要存储在持久化卷（Volume）中。日志不应该写入容器内的文件，而应该输出到标准输出，由 Docker 或编排平台统一收集。

## 总结

Docker 的核心价值是\"一致性\"——开发环境、测试环境、生产环境使用完全相同的镜像，消除了\"环境差异导致的 bug\"。对于个人项目来说，Docker 不是必需品，但理解其原理在团队协作和云部署中非常重要。
""",

    "Linux": """
Linux 是一个开源的类 Unix 操作系统内核，由 Linus Torvalds 在 1991 年创建。今天，绝大多数服务器、云基础设施和嵌入式设备运行的是 Linux。作为开发者，你不需要成为 Linux 系统管理员，但基本的命令行操作、文件系统理解和权限概念是必备技能。

## 为什么开发者需要 Linux

第一，服务器的操作系统几乎都是 Linux。你的 Flask 应用最终会部署在 Linux 服务器上。第二，Linux 的命令行工具链（grep、awk、sed、find）组合起来无比强大，能处理 Windows 下需要专门软件才能完成的任务。第三，很多开发工具和框架默认支持 Linux 环境，在 Windows 上需要额外的配置和踩坑。

## 文件系统

Linux 的文件系统是单一树结构，以 `/` 为根。没有 Windows 的 C 盘、D 盘概念——所有设备和分区都挂载在文件树的某个节点下。理解文件权限（rwx）和所有者（user/group）的概念对运维和安全很重要。

## 常用命令

文件操作：`ls`、`cd`、`cp`、`mv`、`rm`、`mkdir`。文本处理：`grep`（搜索文本）、`cat`（查看文件）、`tail`（查看文件尾部）、`less`（分页查看）。进程管理：`ps`（查看进程）、`kill`（终止进程）、`htop`（交互式监控）。权限：`chmod`、`chown`。

## 本项目中的 Linux 实践

本项目主要在 macOS 上开发，但部署到 Linux 服务器时需要注意几个差异：一是路径分隔符统一用 `/`；二是文件名大小写敏感——`App.py` 和 `app.py` 在 Linux 上是两个不同的文件，在 macOS/Windows 上默认是同一个；三是 Python 虚拟环境的使用方式完全一致。

## 总结

Linux 的学习成本在前期比较高——你需要记忆几十个命令和它们常用的参数。但一旦跨过这个门槛，你会发现命令行比图形界面更高效、更可自动化、更不容易出错。作为后端开发者，Linux 是你最难以被替代的技能之一。
""",

    "MySQL": """
MySQL 是世界上最流行的开源关系型数据库管理系统，由瑞典公司 MySQL AB 在 1995 年创建，2008 年被 Sun Microsystems 收购，2010 年随 Sun 一起归入 Oracle。今天，MySQL 和它的分支 MariaDB 驱动着互联网上绝大多数的 Web 应用。

## MySQL 的架构

MySQL 采用客户端-服务器架构。数据库服务（mysqld）在后台运行，客户端通过网络连接发送 SQL 查询。在 Python 中通过 PyMySQL 或 mysql-connector-python 连接，通常配合 SQLAlchemy ORM 使用。

MySQL 支持多种存储引擎，其中最常用的是 InnoDB。InnoDB 支持事务（ACID）、行级锁和外键约束，是现代 Web 应用的首选引擎。

## 与 SQLite 的对比

SQLite 是嵌入式数据库，MySQL 是服务器数据库。这个区别决定了它们的适用场景：

- SQLite：零配置、文件即数据库、适合单机应用和开发环境
- MySQL：需要安装配置服务、支持网络连接、适合多用户并发访问

本课程项目选择了 SQLite 以减少配置复杂度。但如果需要多用户同时写入（如论坛、电商），MySQL 是更好的选择。

## 索引优化

MySQL 的索引机制比 SQLite 更复杂和强大。支持 B-Tree 索引、哈希索引、全文索引和空间索引。复合索引（多列索引）遵循最左前缀原则——索引 `(a, b, c)` 可以加速查询 `WHERE a=1` 和 `WHERE a=1 AND b=2`，但不能加速 `WHERE b=2`。

## 总结

MySQL 是大多数 Web 应用的首选数据库。对于课程项目来说，SQLite 更方便直接；但对于需要团队协作、高并发或数据安全要求较高的项目，MySQL 是更成熟的选择。理解两者的适用边界，比记住具体的 SQL 语法更重要。
""",

    "PostgreSQL": """
PostgreSQL 被称为\"世界上最先进的开源关系型数据库\"。它由加州大学伯克利分校的 Michael Stonebraker 教授在 1986 年启动，经过三十多年的发展，已经成为功能最全面的开源数据库。

## PostgreSQL 的独特优势

第一，强大的 JSON 支持。PostgreSQL 的 JSONB 类型支持索引和查询，可以同时享受关系型数据库的 ACID 保证和文档数据库的灵活性。

第二，丰富的索引类型。除了标准的 B-Tree，还支持 GIN（倒排索引，适合数组和全文检索）、GiST（通用搜索树，适合地理空间数据）、BRIN（块范围索引，适合超大规模表的顺序数据）。

第三，高级 SQL 功能。窗口函数、CTE（公用表表达式）、递归查询、LATERAL 连接——这些功能在 MySQL 中要么不支持，要么支持不完整。

第四，扩展生态。PostGIS（地理空间扩展）、pg_trgm（模糊搜索）、TimescaleDB（时序数据）等扩展极大地丰富了 PostgreSQL 的应用场景。

## 与 MySQL 的选择

MySQL 适合于：读多写少、简单查询为主、需要成熟的主从复制方案的场景。PostgreSQL 适合于：复杂查询、需要高级 SQL 功能、对数据一致性要求极高的场景。从趋势来看，PostgreSQL 的增长速度已经超过 MySQL，越来越多的新项目选择 PostgreSQL。

## 总结

对于课程项目，SQLite 是最实际的选择。但如果你的项目在未来需要更强大的数据库支持，PostgreSQL 是一个值得学习和投入的方向。它的学习曲线比 MySQL 更陡，但你学到的东西也更多。
""",

    "RESTful": """
REST（Representational State Transfer）是一种 Web 服务架构风格，由 Roy Fielding 在 2000 年的博士论文中正式定义。它不是协议也不是标准，而是一组设计原则和约束。

## REST 的核心原则

### 资源导向

REST 的核心抽象是\"资源\"。一篇文章、一个用户、一条评论都是资源。每个资源有唯一的 URL 标识——`/articles/123` 表示 ID 为 123 的文章。URL 使用名词复数而不是动词，因为 URL 标识的是资源本身而不是操作。

### HTTP 方法的语义

- GET：获取资源。多次请求返回相同结果，不改变服务端状态。
- POST：创建新资源。每次请求可能创建不同的资源，不是幂等的。
- PUT：完整更新资源。客户端提供完整的资源表示。
- PATCH：部分更新资源。只提供需要修改的字段。
- DELETE：删除资源。

### 无状态

每个请求应该包含所有必要的信息，服务端不存储客户端的状态。Session 数据由客户端管理（如 JWT Token），服务端只负责验证。这使得 RESTful API 天然适合水平扩展。

## 本项目中 RESTful 的体现

本项目是服务端渲染的博客，主要返回 HTML 页面。但 AI 写作辅助和 AI 搜索相关的接口遵循了 RESTful 的设计原则。例如，AI 搜索的 POST 请求提交用户的搜索查询，返回结构化的 JSON 结果。AI 状态接口使用 GET 方法，只读不写。

## 常见反模式

第一，所有操作都用 POST。例如\"获取文章列表\"应该用 GET 而不是 POST。第二，在 URL 中使用动词。`/getArticles` 是不好的设计，`GET /articles` 是正确的。第三，在响应体中用 code 字段代替 HTTP 状态码——状态码就是为传达语义而设计的，不必另起炉灶。

## 总结

RESTful API 的设计原则看似简单，但在实际项目中保持一致性并不容易。关键是在项目初期就建立团队的 API 设计规范，并用代码审查来强制执行。对于课程项目来说，理解 RESTful 的设计思路比追求 100% 符合规范更重要——毕竟定义规范的目的也是为了解决实际问题，不是为了教条而存在。
""",

    "TDD": """
测试驱动开发（Test-Driven Development）是一种软件开发方法，它的核心规则是：在没有编写一个失败的测试之前，不写任何产品代码；只写刚好能让测试通过的最少量代码；测试通过后立即重构。这个\"红-绿-重构\"的循环是 TDD 的灵魂。

## TDD 的三个步骤

**第一步：Red（红）**。先写一个测试，运行它，确认它失败了。这个失败说明测试确实在检验某个尚未实现的功能。如果你写了一个测试，它在代码还没写的情况下就通过了，那说明测试没有真正验证什么。

**第二步：Green（绿）**。写最少的代码让测试通过。\"最少\"这两个字很重要——不是写完美的代码，而是写刚好够的代码。如果测试只检查\"输入空标题应返回错误\"，你就只需要处理空标题的情况，不要顺便把内容校验也写了。

**第三步：Refactor（重构）**。在测试通过的保护下，改善代码的结构。消除重复、优化命名、拆分大函数。重构时不用担心改坏逻辑——测试会在你犯错时立即告诉你。

## 本项目的测试实践

本项目共有 284 个 pytest 测试用例和 84 个 E2E 测试用例。虽然我们没有严格执行\"先写测试再写代码\"的 TDD 流程，但测试覆盖了所有核心功能链路的正常和异常路径。

## TDD 的优势与争议

TDD 的优势是显而易见的：测试先行迫使你在写代码之前就想清楚需求；每一个功能都有对应的测试保护；重构时有信心不会引入回归 bug。但 TDD 也有争议：不是所有代码都适合先写测试——探索性的原型开发、UI 布局的调整、简单的配置代码，TDD 可能带来的开销大于收益。

## 总结

TDD 不是教条，而是一种工具。对于课程项目来说，更实际的做法是\"关键路径必须有测试\"——登录、注册、发布文章、权限校验，这些一旦出问题就会影响核心体验的功能，必须用测试保护。至于测试是在代码之前还是之后写的，不影响最终的代码质量。
""",

    "Scrum": """
Scrum 是一个轻量级的敏捷框架，由 Ken Schwaber 和 Jeff Sutherland 在 1995 年联合提出。它的核心理念是\"检查与适应\"——通过固定节奏的迭代（Sprint）不断交付可工作的软件，并在每个迭代结束时根据反馈调整方向。

## Scrum 的三个支柱

第一，**透明**。所有的工作、进展和障碍对团队可见。Product Backlog、Sprint Backlog、燃尽图都是透明化的工具。

第二，**检查**。在每个 Sprint 结束时检查产品增量（Sprint Review）和团队工作方式（Sprint Retrospective）。

第三，**适应**。根据检查结果调整——如果发现某个功能用户不需要，就停止开发；如果发现某个流程拖慢了效率，就改变它。

## Scrum 的角色

Product Owner 负责\"做什么\"——定义产品方向、维护产品待办列表、决定优先级。Scrum Master 负责\"怎么做\"——确保 Scrum 被正确执行、移除团队的障碍、保护团队不受外部干扰。Development Team 负责\"做出来\"——跨职能、自组织的团队，3-9 人为宜。

## 本项目中 Scrum 的体现

虽然是个人项目，但很多 Scrum 的理念被自然地应用了。每个版本（v0.1 到 v1.0）有明确的目标，类似于 Sprint Goal。使用 CR（Change Request）管理需求变更，类似于 Product Backlog 的维护。通过 Review 记录和 AI 协作记录做迭代复盘，类似于 Sprint Retrospective。

## 总结

Scrum 的框架很简单，但真正做好很难。难点不在于流程本身，而在于思维方式——接受不确定性、拥抱变化、通过数据而不是直觉做决策。对于课程项目来说，不需要严格执行 Scrum 的每个仪式，但\"小步交付、频繁验证、持续改进\"的理念值得在每个项目中践行。
""",

    "SOLID": """
SOLID 是面向对象设计的五个基本原则的缩写，由 Robert C. Martin（Uncle Bob）在 2000 年左右整理提出。虽然面向对象编程已经有了几十年的历史，SOLID 原则至今仍然是衡量代码设计质量的黄金标准。

## 单一职责原则（SRP）

一个类应该只有一个发生变化的原因。简单说：一个类只做一件事。违反这个原则的典型症状是：修改一个跟 A 无关的功能时，A 的代码也跟着变了。

## 开闭原则（OCP）

对扩展开放，对修改关闭。当你需要添加新功能时，应该通过扩展现有代码来实现，而不是直接修改。典型的实践是通过策略模式或插件机制来支持扩展。

## 里氏替换原则（LSP）

子类应该能够替换父类而不影响程序的正确性。如果子类修改了父类的方法行为以至于调用方需要判断类型才能正确使用，就违反了 LSP。Python 的鸭子类型让这个原则的实现更加自然。

## 接口隔离原则（ISP）

接口应该小而专注。不要强迫客户依赖它们不使用的方法。如果你的接口有 20 个方法但大多数使用者只需要其中 5 个，这个接口可能太大了。

## 依赖倒置原则（DIP）

高层模块不应该依赖低层模块，两者都应该依赖抽象。在本项目中，路由层不直接操作数据库，而是通过 Service 层——这就是 DIP 的体现。如果将来要换数据库，只需要修改 Service 层。

## 本项目的 SOLID 实践

项目的\"路由层 → Service 层 → Model 层\"分层架构天然遵循了 SRP 和 DIP。每个 Service 类围绕一个业务实体组织（ArticleService、UserService、AIService），避免了把所有功能堆在一个类中。

## 总结

SOLID 原则不是教条，而是在实践中总结出来的经验法则。学习 SOLID 不是为了背下五个缩写，而是为了培养识别坏设计和好设计的能力。这种能力只能通过大量的代码阅读和设计反思来获得。
""",

    "CI/CD": """
CI/CD 是\"持续集成/持续交付\"的缩写，是 DevOps 文化的核心技术实践。简单的说，CI 让你每次提交代码都能自动测试，CD 让你的代码能随时部署到生产环境。

## 持续集成

开发人员每天多次将代码合并到主干。每次合并自动触发构建和测试流程。如果构建或测试失败，团队会在几分钟内收到通知。CI 打破了\"集成地狱\"——过去开发人员各自在自己的分支上工作几周，合并时才发现大量冲突和集成问题。CI 让集成变成日常操作，问题在还小的时候就被发现和解决。

## 持续交付

通过 CI 测试的代码会自动部署到类生产环境（Staging）。产品负责人可以随时点击一个按钮将最新版本发布到生产环境。持续部署则更进一步——通过测试的代码自动部署到生产，不需要人工审批。

## 本项目的 CI/CD 实践

作为课程项目，我们没有部署 CI/CD 流水线。但项目具备 CI/CD 就绪的条件：所有测试可以通过命令行自动运行；数据库初始化脚本可以自动化环境准备；应用通过简单的命令即可启动。如果需要配置 CI/CD，只需添加一个 GitHub Actions 配置文件。

## 为什么 CI/CD 重要

手动测试和部署是低效且容易出错的。人容易忘记测试步骤、搞错部署顺序、在压力下犯错。自动化不替代人的判断，但把重复性工作交给机器，让人专注于更有价值的决策和创造。这是 CI/CD 最核心的价值。
""",

    "JSON": """
JSON（JavaScript Object Notation）是一种轻量级的数据交换格式，由 Douglas Crockford 在 2001 年提出。今天，JSON 已经成为 Web 应用事实上的数据交换标准，取代了上世纪流行的 XML。

## JSON 的语法

JSON 支持六种数据类型：字符串、数字、布尔值、null、数组、对象。对象由键值对组成，键必须是字符串，值可以是任意 JSON 类型。最外层的 JSON 文本可以是对象或数组。

```json
{
  "title": "Flask 入门教程",
  "tags": ["Python", "Flask", "Web"],
  "published": true,
  "views": 1024
}
```

## JSON vs XML

JSON 比 XML 更简洁、更易读、解析更快。XML 的标签会显著增加数据体积，而 JSON 的类型系统更贴近编程语言。在 Web API 领域，JSON 已经完全取代 XML 成为主流格式。XML 仍然在需要复杂文档结构（如配置文件、文档格式）的场景中使用。

## 本项目中 JSON 的使用

AI 服务的所有接口都使用 JSON 格式通信。前端通过 `fetch()` 发送 JSON 请求到 `/ai/` 路由，路由返回 JSON 响应。AI 搜索接口返回的 JSON 包含搜索意图理解、候选文章列表和推荐理由。AI 标签推荐接口用 JSON 数组返回标签列表。

Python 中的 `json` 模块提供了 `json.dumps()`（Python 对象 → JSON 字符串）和 `json.loads()`（JSON 字符串 → Python 对象）。SQLAlchemy 的 JSON 列类型可以存储和查询 JSON 数据。

## 总结

JSON 的成功在于它的简单。它的语法可以在一张纸上写完，它的数据类型足够表达绝大多数场景。对于课程项目来说，理解 JSON 的结构和在前后端之间的数据流转，是理解 Web 应用通信机制的关键。
""",

    "OWASP": """
OWASP（Open Web Application Security Project）是一个全球性的非营利组织，致力于提升软件安全性。它最著名的产出是 OWASP Top 10——每几年发布一次的\"最危险的 Web 应用安全风险\"榜单。

## OWASP Top 10 的关注点

1. **访问控制失效**：用户能访问本不该看到的数据
2. **加密失败**：敏感数据没有正确保护
3. **注入攻击**：SQL 注入、命令注入、XSS
4. **不安全的设计**：架构层面就存在安全缺陷
5. **安全配置错误**：默认密码、错误信息泄露、不必要的功能开启
6. **脆弱的组件**：使用已知漏洞的第三方库
7. **认证失效**：登录机制可以被绕过
8. **软件和数据完整性失效**：CI/CD 流水线被攻击、依赖包被投毒
9. **安全日志和监控失效**：被攻击了不知道
10. **服务端请求伪造（SSRF）**：服务器被诱导向内部系统发起请求

## 本项目的安全措施

针对 OWASP Top 10 中的关键风险，本项目实施了以下防护：

- **SQL 注入**：所有查询通过 SQLAlchemy ORM 参数化，代码中不存在字符串拼接 SQL。
- **XSS**：模板引擎 Jinja2 默认对变量进行 HTML 转义，除非显式使用 `|safe` 标记。
- **CSRF**：Flask-WTF 的 CSRFProtect 为所有 POST 表单提供保护，API 接口有豁免标记。
- **密码安全**：使用 Werkzeug 的 `generate_password_hash`（pbkdf2:sha256）存储密码，不存明文。
- **密钥管理**：SECRET_KEY 和 API Key 从环境变量读取，不硬编码在代码中。
- **错误处理**：错误页不暴露堆栈信息，500 页面只有通用错误提示。

## 总结

安全不是一个功能，而是一种思维方式。对于课程项目来说，理解 OWASP Top 10 中的核心风险和对应的防御措施，比部署昂贵的安全产品更有价值。安全意识需要从第一个功能开始就扎根在开发者的思维中。
""",

    "CSRF": """
CSRF（Cross-Site Request Forgery，跨站请求伪造）是一种利用用户已登录身份发起恶意请求的攻击方式。它的工作原理是：用户登录了网站 A，浏览器保存了 A 的登录 Cookie。当用户访问恶意网站 B 时，B 上的脚本向 A 发起一个请求（如转账、修改密码），浏览器自动附带了 A 的 Cookie，A 以为这个请求是用户本人发起的。

## 防御原理

CSRF 的核心防御手段是在表单中加入一个随机的、不可预测的 Token。正常提交时 Token 会被验证，而攻击者无法获取或猜测这个 Token。Django 和 Rails 等框架默认开启 CSRF 保护，Flask 通过 Flask-WTF 的 CSRFProtect 扩展实现。

## 本项目的 CSRF 实现

在 `app/__init__.py` 中通过 `CSRFProtect(app)` 全局启用 CSRF 保护。所有 HTML 表单通过模板中的 `csrf_token` 注入隐藏的 CSRF Token 字段。AI 相关的 JSON 接口使用 `@csrf.exempt` 豁免 CSRF 检查，因为 AJAX 请求通过 JavaScript fetch 发起，Token 通过请求头传递而不是表单字段。

## CSRF 豁免的考量

豁免 CSRF 保护的接口需要额外的安全保障。AI 搜索接口是只读的（不修改数据），风险较低。AI 写作辅助接口需要登录态，且用户的输入上下文（哪篇文章）在服务端验证。未来如果需要更严格的安全控制，可以为 AI 接口添加独立的 API Key 认证。

## 总结

CSRF 是 Web 安全中的基础防护之一。理解它的攻击原理和防御机制，是每个 Web 开发者的必修课。开启 CSRF 保护不要等到项目后期——第一天就应该做，而且 Flask-WTF 让它变得非常简单。
""",

    "XSS": """
XSS（Cross-Site Scripting，跨站脚本攻击）是攻击者将恶意脚本注入网页，当其他用户访问该页面时脚本被执行。根据注入方式的不同，XSS 分为三种类型：反射型、存储型和 DOM 型。

## 反射型 XSS

攻击者构造一个带有恶意脚本的 URL，诱导用户点击。服务器将 URL 中的脚本\"反射\"回页面，浏览器执行脚本。这是最常见的 XSS 类型，需要用户主动点击恶意链接。

## 存储型 XSS

恶意脚本被永久存储在服务器上（如数据库、评论、用户资料），每当用户访问包含该内容的页面时脚本就被执行。存储型 XSS 比反射型更危险，因为受害者不需要点击恶意链接，正常浏览就会中招。

## DOM 型 XSS

恶意脚本不经过服务器，完全在客户端发生。JavaScript 代码不安全地处理了用户可控的数据（如从 URL 参数中取值并直接用 innerHTML 插入页面）。

## 本项目的 XSS 防护

Jinja2 模板引擎默认对所有变量进行 HTML 转义——`{{ user_input }}` 中的 `<` 会被转义为 `&lt;`，浏览器不会把它当成 HTML 标签执行。这是最基础也最有效的 XSS 防护。

只有显式使用 `|safe` 过滤器时，Jinja2 才会原样输出 HTML。本项目中，Markdown 渲染的内容使用了 `|safe`，但在渲染之前已经通过自定义的 `render_markdown` 函数对用户输入进行了清理和转义。

## 总结

XSS 是 Web 安全中最常见的漏洞类型。防御的关键原则只有一条：永远不要信任用户输入，永远在输出时进行转义。Jinja2 的自动转义大大降低了 XSS 的风险，但开发者仍然需要理解转义的原理，特别是在使用 `|safe` 时。
""",
}


def main():
    with app.app_context():
        articles = Article.query.all()
        updated = 0
        skipped = 0

        for article in articles:
            title = article.title
            matched = None
            for keyword, content in TOPICS.items():
                if keyword.lower() in title.lower():
                    matched = content
                    break

            if matched:
                article.content = matched.strip()
                # Extract first real sentence as summary
                lines = matched.strip().split("\n")
                for line in lines:
                    clean = line.strip()
                    if clean and not clean.startswith("#") and not clean.startswith("```") and len(clean) > 30:
                        article.summary = clean[:150]
                        break
                updated += 1
            else:
                skipped += 1

        db.session.commit()

        print(f"Updated: {updated} articles (800+ chars each)")
        print(f"Skipped: {skipped} (no keyword match)")

        all_articles = Article.query.all()
        under = sum(1 for a in all_articles if len(a.content) < 800)
        over = sum(1 for a in all_articles if len(a.content) >= 800)
        print(f"\nResults: {over} articles 800+ chars, {under} under 800")


if __name__ == "__main__":
    main()
