from datetime import datetime, timedelta
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from app import create_app
from app.extensions import db
from app.models import (
    ARTICLE_STATUS_PUBLISHED,
    COMMENT_STATUS_APPROVED,
    AiLog,
    Article,
    BlogColumn,
    Category,
    Comment,
    Favorite,
    Like,
    Tag,
    User,
)
from app.services import make_slug, utcnow


def user(username, email, nickname, bio, role="user"):
    item = User.query.filter_by(username=username).first()
    if item:
        return item
    item = User(username=username, email=email, nickname=nickname, bio=bio, role=role, status="active")
    item.set_password("user123456" if role == "user" else "admin123456")
    db.session.add(item)
    db.session.flush()
    return item


def get_or_create(model, defaults=None, **kwargs):
    item = model.query.filter_by(**kwargs).first()
    if item:
        return item
    data = dict(kwargs)
    data.update(defaults or {})
    item = model(**data)
    db.session.add(item)
    db.session.flush()
    return item


def create_article(owner, column, category, tags, title, summary, content, days, views=0):
    existing = Article.query.filter_by(title=title).first()
    if existing:
        return existing
    item = Article(
        title=title,
        slug=make_slug(title),
        summary=summary,
        content=content,
        status=ARTICLE_STATUS_PUBLISHED,
        user=owner,
        column=column,
        category=category,
        author=owner.nickname,
        view_count=views,
        published_at=utcnow() - timedelta(days=days),
    )
    item.tags = tags
    db.session.add(item)
    db.session.flush()
    return item


def create_demo_data():
    app = create_app()
    with app.app_context():
        db.create_all()

        admin = user("admin", "admin@example.com", "系统管理员", "负责平台内容、用户和评论管理。", "admin")
        alice = user("alice", "alice@example.com", "林知夏", "记录 Flask、数据库和课程项目实践。")
        bob = user("bob", "bob@example.com", "周远航", "关注算法学习、读书笔记和效率工具。")
        carol = user("carol", "carol@example.com", "陈青禾", "分享前端设计、写作方法和知识管理。")

        categories = {
            "技术实践": get_or_create(Category, name="技术实践", defaults={"description": "工程开发和技术实践。", "sort_order": 1}),
            "学习记录": get_or_create(Category, name="学习记录", defaults={"description": "课程、阅读和复盘记录。", "sort_order": 2}),
            "产品设计": get_or_create(Category, name="产品设计", defaults={"description": "体验、界面和需求分析。", "sort_order": 3}),
        }

        tag_names = ["Flask", "数据库", "软件工程", "Python", "知识管理", "课程实践", "前端设计", "搜索", "阅读笔记", "项目复盘"]
        tags = {name: get_or_create(Tag, name=name) for name in tag_names}

        alice_col = get_or_create(BlogColumn, user_id=alice.id, name="Flask 实践手记", defaults={"description": "从项目骨架到业务闭环的 Flask 开发记录。"})
        bob_col = get_or_create(BlogColumn, user_id=bob.id, name="算法与学习方法", defaults={"description": "把学习过程写成可复用的知识笔记。"})
        carol_col = get_or_create(BlogColumn, user_id=carol.id, name="界面与知识表达", defaults={"description": "关注页面观感、信息组织和写作表达。"})

        articles = [
            create_article(alice, alice_col, categories["技术实践"], [tags["Flask"], tags["软件工程"], tags["Python"]], "从 Flask 骨架到多用户专栏", "记录如何把单人博客升级为多用户知识专栏平台。", "V0.3 的重点是让每个注册用户都能建立自己的专栏、发布文章并参与互动。\n这不是问答社区，而是围绕读博客和写博客展开的知识创作系统。", 1, 42),
            create_article(alice, alice_col, categories["技术实践"], [tags["数据库"], tags["课程实践"]], "SQLite 模型设计中的关系处理", "整理用户、文章、专栏、标签、评论、点赞和收藏之间的关系。", "数据库模型决定后续功能边界。文章属于作者和专栏，标签采用多对多，点赞收藏要限制重复。", 2, 25),
            create_article(alice, alice_col, categories["学习记录"], [tags["项目复盘"], tags["软件工程"]], "软件综合实践第二阶段复盘", "回顾从 V0.1 骨架到 V0.2 业务闭环的开发过程。", "先跑通核心闭环，再逐步加入用户体系和互动功能，是课程项目更稳妥的开发路径。", 4, 19),
            create_article(bob, bob_col, categories["学习记录"], [tags["阅读笔记"], tags["知识管理"]], "如何把阅读笔记整理成博客", "把分散笔记转化为可检索、可维护的知识文章。", "写博客不是为了堆内容，而是为了把阅读、思考和项目经验组织起来，方便未来找回。", 1, 37),
            create_article(bob, bob_col, categories["学习记录"], [tags["搜索"], tags["知识管理"]], "为什么知识系统需要搜索", "搜索是读博客过程中的关键能力。", "用户读博客的第一性需求是找到自己需要的知识，因此搜索要覆盖标题、摘要、正文、作者和标签。", 3, 31),
            create_article(bob, bob_col, categories["技术实践"], [tags["Python"], tags["课程实践"]], "用小脚本验证业务流程", "用脚本和测试客户端快速验证路由和权限。", "课程项目也需要基本验证，至少要确认首页、登录、权限、评论和后台页面不会报错。", 5, 16),
            create_article(carol, carol_col, categories["产品设计"], [tags["前端设计"], tags["知识管理"]], "知识博客首页应该展示什么", "首页要帮助用户理解平台定位并快速进入阅读和创作。", "多用户知识博客首页应展示最新文章、推荐专栏、热门分类、热门标签和活跃作者，而不是商业化信息流。", 2, 44),
            create_article(carol, carol_col, categories["产品设计"], [tags["前端设计"], tags["项目复盘"]], "表单和卡片的统一设计", "统一按钮、表单、卡片和提示信息，让系统看起来更完整。", "页面不需要复杂前端工程化，但要有一致的视觉语言，让课程演示更可信。", 6, 13),
        ]

        if not Comment.query.first():
            db.session.add_all(
                [
                    Comment(article=articles[0], user=bob, nickname=bob.nickname, email=bob.email, content="这个升级方向比单人博客更适合课程演示。", status=COMMENT_STATUS_APPROVED),
                    Comment(article=articles[0], user=carol, nickname=carol.nickname, email=carol.email, content="专栏和作者主页可以体现多用户创作平台定位。", status=COMMENT_STATUS_APPROVED),
                    Comment(article=articles[3], user=alice, nickname=alice.nickname, email=alice.email, content="把阅读笔记结构化确实很重要。", status=COMMENT_STATUS_APPROVED),
                    Comment(article=articles[6], user=bob, nickname=bob.nickname, email=bob.email, content="首页信息层级清楚很多。", status=COMMENT_STATUS_APPROVED),
                ]
            )

        pairs = [(alice, articles[3]), (alice, articles[6]), (bob, articles[0]), (bob, articles[6]), (carol, articles[0]), (carol, articles[4])]
        for owner, article in pairs:
            if not Like.query.filter_by(user_id=owner.id, article_id=article.id).first():
                db.session.add(Like(user=owner, article=article))
                article.like_count += 1
            if not Favorite.query.filter_by(user_id=owner.id, article_id=article.id).first():
                db.session.add(Favorite(user=owner, article=article))
                article.favorite_count += 1

        if not AiLog.query.first():
            db.session.add(
                AiLog(
                    article=articles[0],
                    scene="placeholder",
                    input_text="V0.3 仍不调用真实 AI 接口。",
                    ai_output="AI 功能将在后续版本开放。",
                    problem_found="当前仅作为扩展点记录。",
                )
            )

        db.session.commit()
        print("V0.3 演示数据写入完成。")
        print("管理员：admin / admin123456")
        print("普通用户：alice / user123456, bob / user123456, carol / user123456")


if __name__ == "__main__":
    create_demo_data()
