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
    ARTICLE_STATUS_DRAFT,
    ARTICLE_STATUS_PUBLISHED,
    COMMENT_STATUS_APPROVED,
    COMMENT_STATUS_PENDING,
    AiLog,
    Article,
    Category,
    Comment,
    Tag,
    User,
)
from app.services import make_slug


def get_or_create(model, defaults=None, **kwargs):
    instance = model.query.filter_by(**kwargs).first()
    if instance:
        return instance
    params = dict(kwargs)
    params.update(defaults or {})
    instance = model(**params)
    db.session.add(instance)
    db.session.flush()
    return instance


def ensure_admin():
    admin = User.query.filter_by(username="admin").first()
    if not admin:
        admin = User(username="admin", nickname="系统管理员", role="admin", status="active")
        admin.set_password("admin123456")
        db.session.add(admin)


def create_demo_data():
    app = create_app()
    with app.app_context():
        db.create_all()
        ensure_admin()

        tech = get_or_create(
            Category,
            name="技术实践",
            defaults={
                "description": "记录 Flask、数据库、软件工程等实践内容。",
                "sort_order": 1,
            },
        )
        life = get_or_create(
            Category,
            name="学习记录",
            defaults={
                "description": "保存课程实践、阶段复盘和学习笔记。",
                "sort_order": 2,
            },
        )

        flask = get_or_create(Tag, name="Flask")
        database = get_or_create(Tag, name="数据库")
        engineering = get_or_create(Tag, name="软件工程")
        review = get_or_create(Tag, name="阶段复盘")

        if not Article.query.filter_by(title="用 Flask 搭建个人博客系统骨架").first():
            article = Article(
                title="用 Flask 搭建个人博客系统骨架",
                slug=make_slug("用 Flask 搭建个人博客系统骨架"),
                summary="记录第一阶段如何完成 Flask app factory、Blueprint、模板和运行入口。",
                content=(
                    "第一阶段的重点不是追求功能数量，而是先让系统具备清晰的工程骨架。\n"
                    "项目采用 Flask app factory 创建应用，并使用 Blueprint 为后续模块拆分做准备。\n"
                    "通过 extensions.py 统一管理 SQLAlchemy 和 Flask-Login，可以减少循环导入风险。\n"
                    "这个基础结构让后续文章、分类、标签、评论和后台管理都能稳定扩展。"
                ),
                status=ARTICLE_STATUS_PUBLISHED,
                category=tech,
                author="管理员",
                view_count=18,
                published_at=datetime.utcnow() - timedelta(days=1),
            )
            article.tags = [flask, engineering]
            db.session.add(article)

        if not Article.query.filter_by(title="为什么先做非 AI 的博客业务闭环").first():
            article = Article(
                title="为什么先做非 AI 的博客业务闭环",
                slug=make_slug("为什么先做非 AI 的博客业务闭环"),
                summary="V0.2 先把文章、分类、标签、评论和后台管理跑通，AI 在后续版本接入。",
                content=(
                    "AI 功能是这个项目后续的重要扩展点，但系统首先需要一个可靠的业务底座。\n"
                    "如果文章管理、分类标签、评论审核和后台权限没有跑通，AI 输出也无法被稳定使用。\n"
                    "因此 V0.2 把重点放在非 AI 的完整闭环上，并为 V0.3 预留 AI 服务接口。"
                ),
                status=ARTICLE_STATUS_PUBLISHED,
                category=life,
                author="管理员",
                view_count=9,
                published_at=datetime.utcnow() - timedelta(hours=10),
            )
            article.tags = [engineering, review]
            db.session.add(article)

        if not Article.query.filter_by(title="数据库模型设计草稿").first():
            article = Article(
                title="数据库模型设计草稿",
                slug=make_slug("数据库模型设计草稿"),
                summary="这是一篇后台可见的草稿文章，用于演示文章状态管理。",
                content="草稿文章不会显示在前台，只能在后台文章管理中查看和编辑。",
                status=ARTICLE_STATUS_DRAFT,
                category=tech,
                author="管理员",
            )
            article.tags = [database]
            db.session.add(article)

        db.session.flush()

        first_article = Article.query.filter_by(title="用 Flask 搭建个人博客系统骨架").first()
        if first_article and not Comment.query.filter_by(article_id=first_article.id).first():
            db.session.add(
                Comment(
                    article=first_article,
                    nickname="课程观察员",
                    email="reviewer@example.com",
                    content="结构清晰，后续可以继续补业务功能。",
                    status=COMMENT_STATUS_APPROVED,
                )
            )
            db.session.add(
                Comment(
                    article=first_article,
                    nickname="待审核用户",
                    email="pending@example.com",
                    content="这是一条待审核评论，用于演示后台评论审核。",
                    status=COMMENT_STATUS_PENDING,
                )
            )

        if not AiLog.query.first():
            db.session.add(
                AiLog(
                    article=first_article,
                    scene="placeholder",
                    input_text="V0.2 不调用真实 AI 接口。",
                    ai_output="AI 功能将在后续版本开放。",
                    problem_found="当前仅作为扩展点记录。",
                )
            )

        db.session.commit()
        print("演示数据写入完成。")
        print("可使用 admin / admin123456 登录后台。")


if __name__ == "__main__":
    create_demo_data()
