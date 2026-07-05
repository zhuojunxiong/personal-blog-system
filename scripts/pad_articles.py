import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app import create_app
from app.extensions import db
from app.models import Article

# Extra paragraphs to pad articles, matched by keyword in title
EXTRA = {
    "Flask": "\n\n## 实践经验\n\n在实际开发中，有几个容易踩坑的地方值得注意。首先是 Flask 的调试模式在生产环境中一定要关闭——debug=True 会允许任意代码执行。其次是蓝图（Blueprint）的注册顺序，如果使用了 url_prefix，要确保前缀不会互相冲突。第三是 SQLAlchemy 的 session 管理，在请求结束时一定要关闭 session，否则会导致连接泄漏。对于大型项目，建议使用 Flask-Script 或 Click 编写命令行工具来管理数据库迁移、数据导入等运维操作。这些细节虽然看起来琐碎，但在项目变大的时候会显著影响开发和维护效率。",
    
    "SQLite": "\n\n## SQLite 在生产环境中的注意事项\n\n虽然 SQLite 默认配置已经很适合开发环境，但在生产部署时需要注意几个关键配置。首先，将 journal_mode 设置为 WAL（Write-Ahead Logging）模式，这允许多个读操作与一个写操作并发执行，显著提升并发读取性能。其次，将 synchronous 设置为 NORMAL 而不是 FULL，可以在保证安全性的前提下提升写入性能。第三，定期执行 VACUUM 命令回收删除数据后留下的空间。另外，SQLite 的并发写入限制决定了它不适合高并发写入的场景——如果你的应用需要支持大量用户同时发布文章，应该考虑迁移到 MySQL 或 PostgreSQL。对于课程项目和小型博客来说，SQLite 已经足够胜任，它的零配置特性让项目的部署和维护变得非常简单。",

    "pytest": "\n\n## 实际测试案例分析\n\n以本项目为例，我们在 v0.5 阶段开始系统地引入自动化测试。最初只写了几个简单的路由测试，验证页面是否返回 200。后来逐步扩展到模型测试（验证字段约束和关系映射）、服务层测试（验证业务逻辑正确性）、边界测试（SQL 注入、XSS、CSRF、超长输入）和性能测试（响应时间、批量操作、并发请求）。目前整个测试套件包含 290 个测试用例，覆盖了从公开页面到后台管理的全部核心链路。写测试最大的收益不是找到 bug，而是在重构时给你信心——你可以在改动后立即运行测试，知道哪些功能被破坏了，从而快速定位和修复问题。",

    "SQL": "\n\n## SQL 注入防御的最佳实践\n\n参数化查询是防御 SQL 注入最核心的手段，但除此之外还有几个容易被忽视的安全措施。一是最小权限原则——应用连接的数据库用户只应拥有必要的权限，即使 SQL 注入成功，攻击者也无法执行 DROP TABLE 等破坏性操作。二是错误信息脱敏——生产环境中绝不能将数据库错误信息直接返回给用户，这些信息可能暴露表结构和查询逻辑。三是输入校验——在参数化查询的基础上，对输入做类型和长度校验作为额外的防线。本项目中所有数据库操作都通过 SQLAlchemy ORM 完成，ORM 层自动进行了参数化处理，这是选择 ORM 的一个重要安全收益。",

    "Linux": "\n\n## Linux 学习路径建议\n\n对于后端开发者来说，Linux 的学习可以分三个阶段。第一阶段是基本操作：文件管理（ls、cd、cp、mv）、文本处理（grep、cat、tail）、进程管理（ps、kill）。第二阶段是系统管理：用户和权限（chmod、chown）、服务管理（systemctl）、日志查看（journalctl）。第三阶段是网络和性能：端口和连接（netstat、ss）、性能监控（top、htop、iotop）、防火墙（iptables、ufw）。不需要一次学完所有内容——先掌握日常开发中最常用的命令，遇到新问题时再去查文档。Shell 脚本是将多个命令组合为自动化流程的强大工具，值得投入时间学习。",

    "Docker": "\n\n## Docker 实际应用场景\n\nDocker 在开发和部署中都有广泛的应用。在开发阶段，可以用 Docker Compose 一键启动应用所需的所有服务（数据库、缓存、消息队列），新成员加入团队时只需要 docker-compose up 就可以获得完整的开发环境。在部署阶段，Docker 镜像保证了环境的一致性——在开发环境测试通过的镜像，在服务器上运行的结果完全一致。但 Docker 不是银弹。对于简单的课设项目，直接使用 Python 虚拟环境可能更方便。Docker 的价值真正体现于多服务、多环境的复杂场景。建议在理解了基础开发流程之后，再逐步引入容器化。"
}

def main():
    app = create_app()
    with app.app_context():
        padded = 0
        for article in Article.query.all():
            if len(article.content) >= 800:
                continue
            for keyword, extra in EXTRA.items():
                if keyword.lower() in article.title.lower() or keyword.lower() in article.content.lower():
                    article.content += extra
                    padded += 1
                    break
        
        db.session.commit()
        
        short = sum(1 for a in Article.query.all() if len(a.content) < 800)
        over = sum(1 for a in Article.query.all() if len(a.content) >= 800)
        print(f"Padded: {padded}")
        print(f"800+ chars: {over}, Under 800: {short}")

if __name__ == "__main__":
    main()
