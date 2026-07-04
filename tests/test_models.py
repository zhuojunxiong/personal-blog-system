"""Unit tests for data models."""
import pytest
from app.models import (
    ARTICLE_STATUS_DRAFT,
    ARTICLE_STATUS_PUBLISHED,
    COMMENT_STATUS_APPROVED,
    COMMENT_STATUS_HIDDEN,
    COMMENT_STATUS_PENDING,
    Article,
    BlogColumn,
    Category,
    Comment,
    Favorite,
    Like,
    Tag,
    User,
)
from app.extensions import db
from app.services import make_slug, utcnow


def _make_user_simple(username, email, **kwargs):
    """Minimal user creator for model tests."""
    u = User(username=username, email=email, **kwargs)
    u.set_password("testpass123")
    return u


class TestUserModel:
    """Tests for the User model."""

    def test_create_user(self, app, normal_user):
        u = User.query.filter_by(username="alice").first()
        assert u is not None
        assert u.email == "alice@example.com"
        assert u.nickname == "林知夏"
        assert u.role == "user"
        assert u.status == "active"
        assert u.is_active is True
        assert u.is_admin is False

    def test_admin_user(self, app, admin_user):
        u = User.query.filter_by(username="admin").first()
        assert u.is_admin is True
        assert u.role == "admin"

    def test_password_hashing(self, app, normal_user):
        u = User.query.filter_by(username="alice").first()
        assert u.check_password("user123456") is True
        assert u.check_password("wrong_password") is False

    def test_password_not_stored_plaintext(self, app, normal_user):
        u = User.query.filter_by(username="alice").first()
        assert u.password_hash != "user123456"
        assert u.password_hash.startswith("pbkdf2:sha256")

    def test_set_password(self, app):
        u = _make_user_simple("newuser", "new@test.com", nickname="新用户")
        u.set_password("mypassword")
        db.session.add(u)
        db.session.commit()
        assert u.check_password("mypassword") is True

    def test_user_unique_constraints(self, app, normal_user):
        dup = _make_user_simple("alice", "other@test.com")
        db.session.add(dup)
        with pytest.raises(Exception):
            db.session.commit()
        db.session.rollback()

    def test_inactive_user(self, app):
        u = _make_user_simple("inactive", "inactive@test.com", status="disabled")
        db.session.add(u)
        db.session.commit()
        assert u.is_active is False

    def test_user_profile_markdown(self, app):
        u = _make_user_simple("mduser", "md@test.com",
            profile_markdown="# 我的主页\n\n这是个人介绍。")
        db.session.add(u)
        db.session.commit()
        assert u.profile_markdown == "# 我的主页\n\n这是个人介绍。"


class TestArticleModel:
    """Tests for the Article model."""

    def test_create_article(self, app, published_article, normal_user, category):
        a = Article.query.first()
        assert a is not None
        assert a.title == "Flask 入门指南"
        assert a.status == ARTICLE_STATUS_PUBLISHED
        assert a.user_id == normal_user.id
        assert a.category_id == category.id

    def test_article_slug_generation(self, app, published_article):
        a = Article.query.first()
        assert a.slug is not None
        assert len(a.slug) > 0

    def test_article_defaults(self, app, category, normal_user):
        a = Article(
            title="测试文章",
            slug=make_slug("测试文章"),
            content="内容",
            category_id=category.id,
            user_id=normal_user.id,
        )
        db.session.add(a)
        db.session.commit()
        assert a.status == ARTICLE_STATUS_DRAFT
        assert a.view_count == 0
        assert a.like_count == 0
        assert a.favorite_count == 0

    def test_article_draft_status(self, app, draft_article):
        a = Article.query.filter_by(status=ARTICLE_STATUS_DRAFT).first()
        assert a is not None
        assert a.published_at is None

    def test_article_published_status(self, app, published_article):
        a = Article.query.filter_by(status=ARTICLE_STATUS_PUBLISHED).first()
        assert a is not None
        assert a.published_at is not None

    def test_approved_comment_count(self, app, published_article):
        a = Article.query.first()
        assert a.approved_comment_count == 0

        c = Comment(
            article_id=a.id, nickname="评论者", email="c@test.com",
            content="好文章", status=COMMENT_STATUS_APPROVED,
        )
        db.session.add(c)
        db.session.commit()
        assert a.approved_comment_count == 1

        c2 = Comment(
            article_id=a.id, nickname="评论者2", email="c2@test.com",
            content="待审核", status=COMMENT_STATUS_PENDING,
        )
        db.session.add(c2)
        db.session.commit()
        assert a.approved_comment_count == 1  # Pending not counted


class TestCategoryModel:
    """Tests for the Category model."""

    def test_create_category(self, app, category):
        c = Category.query.first()
        assert c.name == "技术实践"
        assert c.description == "工程开发和技术实践"
        assert c.sort_order == 1

    def test_category_unique_name(self, app, category):
        dup = Category(name="技术实践")
        db.session.add(dup)
        with pytest.raises(Exception):
            db.session.commit()
        db.session.rollback()


class TestTagModel:
    """Tests for the Tag model."""

    def test_create_tag(self, app, tag):
        t = Tag.query.first()
        assert t.name == "Python"

    def test_tag_unique_name(self, app, tag):
        dup = Tag(name="Python")
        db.session.add(dup)
        with pytest.raises(Exception):
            db.session.commit()
        db.session.rollback()

    def test_tag_article_relationship(self, app, published_article, tag):
        a = Article.query.first()
        t = Tag.query.first()
        a.tags.append(t)
        db.session.commit()
        assert t in a.tags
        assert a in t.articles


class TestCommentModel:
    """Tests for the Comment model."""

    def test_create_comment(self, app, approved_comment):
        c = Comment.query.first()
        assert c.status == COMMENT_STATUS_APPROVED
        assert "教程" in c.content

    def test_comment_statuses(self, app, published_article):
        a = Article.query.first()
        c1 = Comment(article_id=a.id, nickname="u1", email="u1@t.com",
                     content="test1", status=COMMENT_STATUS_PENDING)
        c2 = Comment(article_id=a.id, nickname="u2", email="u2@t.com",
                     content="test2", status=COMMENT_STATUS_HIDDEN)
        db.session.add_all([c1, c2])
        db.session.commit()
        assert Comment.query.filter_by(status=COMMENT_STATUS_PENDING).count() == 1
        assert Comment.query.filter_by(status=COMMENT_STATUS_HIDDEN).count() == 1


class TestLikeModel:
    """Tests for the Like model."""

    def test_create_like(self, app, published_article, normal_user):
        like = Like(user_id=normal_user.id, article_id=published_article.id)
        db.session.add(like)
        db.session.commit()
        assert Like.query.count() == 1

    def test_unique_like_constraint(self, app, published_article, normal_user):
        like1 = Like(user_id=normal_user.id, article_id=published_article.id)
        db.session.add(like1)
        db.session.commit()
        like2 = Like(user_id=normal_user.id, article_id=published_article.id)
        db.session.add(like2)
        with pytest.raises(Exception):
            db.session.commit()
        db.session.rollback()


class TestFavoriteModel:
    """Tests for the Favorite model."""

    def test_create_favorite(self, app, published_article, normal_user):
        fav = Favorite(user_id=normal_user.id, article_id=published_article.id)
        db.session.add(fav)
        db.session.commit()
        assert Favorite.query.count() == 1

    def test_unique_favorite_constraint(self, app, published_article, normal_user):
        fav1 = Favorite(user_id=normal_user.id, article_id=published_article.id)
        db.session.add(fav1)
        db.session.commit()
        fav2 = Favorite(user_id=normal_user.id, article_id=published_article.id)
        db.session.add(fav2)
        with pytest.raises(Exception):
            db.session.commit()
        db.session.rollback()


class TestBlogColumnModel:
    """Tests for the BlogColumn model."""

    def test_create_column(self, app, column):
        c = BlogColumn.query.first()
        assert c.name == "Flask 实践手记"
        assert c.status == "active"

    def test_column_user_relationship(self, app, column, normal_user):
        c = BlogColumn.query.first()
        assert c.user_id == normal_user.id
        assert c.user.username == "alice"
