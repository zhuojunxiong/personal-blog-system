"""Pytest fixtures for the blog system test suite."""
import pytest
from app import create_app
from app.extensions import db
from app.models import (
    ARTICLE_STATUS_DRAFT,
    ARTICLE_STATUS_PUBLISHED,
    COMMENT_STATUS_APPROVED,
    COMMENT_STATUS_PENDING,
    Article,
    BlogColumn,
    Category,
    Comment,
    Tag,
    User,
)
from app.services import make_slug, utcnow


@pytest.fixture(scope="function")
def app():
    """Create a fresh app with an in-memory SQLite database for each test."""
    test_app = create_app()
    test_app.config["TESTING"] = True
    test_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    test_app.config["WTF_CSRF_ENABLED"] = False
    test_app.config["SERVER_NAME"] = "localhost"
    test_app.config["AI_ENABLED"] = False  # Disable AI for tests

    # Prevent objects from being expired after commit so they can be
    # shared across fixtures without DetachedInstanceError.
    test_app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "connect_args": {"check_same_thread": False}
    }

    with test_app.app_context():
        db.create_all()
        yield test_app
        db.session.rollback()
        db.drop_all()


@pytest.fixture(scope="function")
def client(app):
    """Flask test client."""
    return app.test_client()


@pytest.fixture(scope="function")
def runner(app):
    """Flask CLI test runner."""
    return app.test_cli_runner()


# ============================================================
# Database seed fixtures
# All fixtures run within the app's context provided by the `app` fixture.
# We use db.session.commit() so data is visible to the test client,
# and wrap in try/finally to ensure rollback on error.
# Objects are refreshed after commit to prevent DetachedInstanceError
# when fixtures depend on each other.
# ============================================================


def _make_user(**kwargs):
    """Helper to create a user, commit, then refresh."""
    password = kwargs.pop("password", "user123456")
    u = User(**kwargs)
    u.set_password(password)
    db.session.add(u)
    db.session.commit()
    return u


@pytest.fixture(scope="function")
def admin_user(app):
    """Create an admin user."""
    return _make_user(
        username="admin",
        email="admin@example.com",
        nickname="系统管理员",
        role="admin",
        status="active",
        bio="平台管理员",
        password="admin123456",
    )


@pytest.fixture(scope="function")
def normal_user(app):
    """Create a normal user."""
    return _make_user(
        username="alice",
        email="alice@example.com",
        nickname="林知夏",
        role="user",
        status="active",
        bio="全栈开发者",
    )


@pytest.fixture(scope="function")
def second_user(app):
    """Create a second normal user."""
    return _make_user(
        username="bob",
        email="bob@example.com",
        nickname="周远航",
        role="user",
        status="active",
        bio="算法工程师",
    )


@pytest.fixture(scope="function")
def category(app):
    """Create a default category."""
    cat = Category(name="技术实践", description="工程开发和技术实践", sort_order=1)
    db.session.add(cat)
    db.session.commit()
    return cat


@pytest.fixture(scope="function")
def tag(app):
    """Create a default tag."""
    t = Tag(name="Python")
    db.session.add(t)
    db.session.commit()
    return t


@pytest.fixture(scope="function")
def published_article(app, normal_user, category):
    """Create a published article."""
    article = Article(
        title="Flask 入门指南",
        slug=make_slug("Flask 入门指南"),
        summary="一篇 Flask 入门教程",
        content="这是文章的正文内容，详细介绍了 Flask 框架的基础知识。",
        status=ARTICLE_STATUS_PUBLISHED,
        user_id=normal_user.id,
        category_id=category.id,
        author=normal_user.nickname,
        published_at=utcnow(),
    )
    db.session.add(article)
    db.session.commit()
    return article


@pytest.fixture(scope="function")
def draft_article(app, normal_user, category):
    """Create a draft article."""
    article = Article(
        title="未完成的草稿",
        slug=make_slug("未完成的草稿"),
        summary="还在写",
        content="草稿内容...",
        status=ARTICLE_STATUS_DRAFT,
        user_id=normal_user.id,
        category_id=category.id,
        author=normal_user.nickname,
    )
    db.session.add(article)
    db.session.commit()
    return article


@pytest.fixture(scope="function")
def column(app, normal_user):
    """Create a blog column."""
    col = BlogColumn(
        user_id=normal_user.id,
        name="Flask 实践手记",
        description="从骨架到闭环的 Flask 记录",
        status="active",
    )
    db.session.add(col)
    db.session.commit()
    return col


@pytest.fixture(scope="function")
def approved_comment(app, published_article, normal_user):
    """Create an approved comment."""
    comment = Comment(
        article_id=published_article.id,
        user_id=normal_user.id,
        nickname=normal_user.nickname,
        email=normal_user.email,
        content="这是一条很棒的教程！",
        status=COMMENT_STATUS_APPROVED,
    )
    db.session.add(comment)
    db.session.commit()
    return comment


# ============================================================
# Login helpers
# ============================================================


def login(client, username, password):
    """Helper to log in a user."""
    return client.post(
        "/login",
        data={"username": username, "password": password},
        follow_redirects=True,
    )


def login_admin(client):
    """Log in as admin."""
    return login(client, "admin", "admin123456")


def login_alice(client):
    """Log in as alice (normal_user)."""
    return login(client, "alice", "user123456")


def login_bob(client):
    """Log in as bob (second_user)."""
    return login(client, "bob", "user123456")


def logout(client):
    """Log out current user."""
    return client.get("/logout", follow_redirects=True)
