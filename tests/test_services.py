"""Unit tests for service classes."""
import pytest
from app.article.services import ArticleService
from app.auth.services import AuthService
from app.category.services import CategoryService
from app.column.services import ColumnService
from app.comment.services import CommentService
from app.dashboard.services import DashboardService
from app.tag.services import TagService
from app.user.services import UserService
from app.extensions import db
from app.models import (
    ARTICLE_STATUS_DRAFT,
    ARTICLE_STATUS_PUBLISHED,
    AI_REVIEW_STATUS_PENDING,
    AI_REVIEW_STATUS_UNAVAILABLE,
    COMMENT_STATUS_APPROVED,
    COMMENT_STATUS_PENDING,
    Article,
    BlogColumn,
    Category,
    Comment,
    Tag,
)
from tests.conftest import login_alice


# ============================================================
# AuthService Tests
# ============================================================


class TestAuthService:
    def test_validate_register_valid(self, app):
        with app.app_context():
            data = {
                "username": "newuser",
                "email": "new@test.com",
                "password": "password123",
                "nickname": "新用户",
            }
            errors = AuthService.validate_register(data)
            assert len(errors) == 0

    def test_validate_register_empty_username(self, app):
        with app.app_context():
            errors = AuthService.validate_register({"username": "", "email": "a@b.com", "password": "123456"})
            assert any("用户名" in e for e in errors)

    def test_validate_register_invalid_email(self, app):
        with app.app_context():
            errors = AuthService.validate_register({"username": "test", "email": "notanemail", "password": "123456"})
            assert any("邮箱" in e for e in errors)

    def test_validate_register_short_password(self, app):
        with app.app_context():
            errors = AuthService.validate_register({"username": "test", "email": "a@b.com", "password": "123"})
            assert any("密码" in e for e in errors)

    def test_validate_register_duplicate_username(self, app, normal_user):
        with app.app_context():
            errors = AuthService.validate_register({"username": "alice", "email": "new@b.com", "password": "123456"})
            assert any("用户名已存在" in e for e in errors)

    def test_validate_register_duplicate_email(self, app, normal_user):
        with app.app_context():
            errors = AuthService.validate_register({"username": "newuser", "email": "alice@example.com", "password": "123456"})
            assert any("邮箱已被注册" in e for e in errors)

    def test_register_success(self, app):
        with app.app_context():
            data = {"username": "newuser", "email": "new@test.com", "password": "password123"}
            user, errors = AuthService.register(data)
            assert len(errors) == 0
            assert user is not None
            assert user.username == "newuser"
            assert user.role == "user"
            assert user.status == "active"

    def test_register_duplicate(self, app, normal_user):
        with app.app_context():
            data = {"username": "alice", "email": "alice@example.com", "password": "password123"}
            user, errors = AuthService.register(data)
            assert user is None
            assert len(errors) > 0


# ============================================================
# ArticleService Tests
# ============================================================


class TestArticleService:
    def test_validate_valid(self, app, category):
        with app.app_context():
            data = {
                "title": "测试文章",
                "summary": "测试摘要",
                "content": "测试正文内容",
                "category_id": str(category.id),
                "status": ARTICLE_STATUS_PUBLISHED,
            }
            errors = ArticleService.validate(data)
            assert len(errors) == 0

    def test_validate_empty_title(self, app, category):
        with app.app_context():
            data = {"title": "", "content": "内容", "category_id": str(category.id)}
            errors = ArticleService.validate(data)
            assert any("标题不能为空" in e for e in errors)

    def test_validate_empty_content(self, app, category):
        with app.app_context():
            data = {"title": "标题", "content": "", "category_id": str(category.id)}
            errors = ArticleService.validate(data)
            assert any("正文不能为空" in e for e in errors)

    def test_validate_no_category(self, app):
        with app.app_context():
            data = {"title": "标题", "content": "内容", "category_id": ""}
            errors = ArticleService.validate(data)
            assert any("分类" in e for e in errors)

    def test_validate_nonexistent_category(self, app):
        with app.app_context():
            data = {"title": "标题", "content": "内容", "category_id": "99999"}
            errors = ArticleService.validate(data)
            assert any("分类不存在" in e for e in errors)

    def test_validate_title_max_length(self, app, category):
        with app.app_context():
            data = {"title": "a" * 200, "content": "内容", "category_id": str(category.id)}
            errors = ArticleService.validate(data)
            assert any("160" in e for e in errors or [""])

    def test_create_article(self, app, normal_user, category):
        with app.app_context():
            data = {
                "title": "新文章",
                "summary": "摘要",
                "content": "正文内容很多",
                "category_id": str(category.id),
                "status": ARTICLE_STATUS_PUBLISHED,
            }
            article, errors = ArticleService.create(data, [], user=normal_user)
            assert len(errors) == 0
            assert article is not None
            assert article.title == "新文章"
            assert article.user_id == normal_user.id
            assert article.status == ARTICLE_STATUS_PUBLISHED
            assert article.published_at is not None
            assert article.ai_review_status == AI_REVIEW_STATUS_UNAVAILABLE
            assert "AI 接口已关闭" in article.ai_review_reason

    def test_create_draft(self, app, normal_user, category):
        with app.app_context():
            data = {
                "title": "草稿文章",
                "content": "草稿内容",
                "category_id": str(category.id),
                "status": ARTICLE_STATUS_DRAFT,
            }
            article, errors = ArticleService.create(data, [], user=normal_user)
            assert len(errors) == 0
            assert article.status == ARTICLE_STATUS_DRAFT
            assert article.published_at is None
            assert article.ai_review_status == AI_REVIEW_STATUS_PENDING

    def test_update_article(self, app, published_article, category):
        with app.app_context():
            a = Article.query.first()
            data = {
                "title": "更新后的标题",
                "summary": "更新摘要",
                "content": "更新后的正文内容",
                "category_id": str(category.id),
                "status": ARTICLE_STATUS_PUBLISHED,
            }
            errors = ArticleService.update(a, data, [])
            assert len(errors) == 0
            assert a.title == "更新后的标题"
            assert a.summary == "更新摘要"

    def test_delete_article(self, app, published_article):
        with app.app_context():
            a = Article.query.first()
            ArticleService.delete(a)
            assert Article.query.count() == 0

    def test_increment_view(self, app, published_article):
        with app.app_context():
            a = Article.query.first()
            old_views = a.view_count
            ArticleService.increment_view(a)
            assert a.view_count == old_views + 1

    def test_toggle_like(self, app, published_article, normal_user):
        with app.app_context():
            a = Article.query.first()
            u = UserService.get_or_404(normal_user.id)
            # First toggle -> like
            result = ArticleService.toggle_like(a, u)
            assert result is True
            assert a.like_count == 1
            # Second toggle -> unlike
            result = ArticleService.toggle_like(a, u)
            assert result is False
            assert a.like_count == 0

    def test_toggle_favorite(self, app, published_article, normal_user):
        with app.app_context():
            a = Article.query.first()
            u = UserService.get_or_404(normal_user.id)
            # First toggle -> favorite
            result = ArticleService.toggle_favorite(a, u)
            assert result is True
            assert a.favorite_count == 1
            # Second toggle -> unfavorite
            result = ArticleService.toggle_favorite(a, u)
            assert result is False
            assert a.favorite_count == 0

    def test_liked_by_not_authenticated(self, app, published_article):
        with app.app_context():
            a = Article.query.first()
            # Anonymous user (not authenticated)
            from flask_login import AnonymousUserMixin
            anon = type("Anon", (AnonymousUserMixin,), {})()
            assert ArticleService.liked_by(a, anon) is False

    def test_list_published(self, app, published_article, draft_article):
        with app.app_context():
            pagination = ArticleService.list_published(page=1)
            assert pagination.total >= 1
            # All items should be published
            for item in pagination.items:
                assert item.status == ARTICLE_STATUS_PUBLISHED

    def test_search_published(self, app, published_article):
        with app.app_context():
            pagination = ArticleService.search_published("Flask", page=1)
            assert pagination.total >= 1

    def test_search_no_results(self, app, published_article):
        with app.app_context():
            pagination = ArticleService.search_published("xyz_nonexistent_12345", page=1)
            assert pagination.total == 0

    def test_unique_slug(self, app, category, normal_user):
        with app.app_context():
            slug1 = ArticleService.unique_slug("Flask 入门")
            # Create article with that slug
            a = Article(
                title="Flask 入门", slug=slug1, content="test",
                category_id=category.id, user_id=normal_user.id,
            )
            db.session.add(a)
            db.session.commit()
            # Next slug should be different
            slug2 = ArticleService.unique_slug("Flask 入门")
            assert slug2 != slug1

    def test_get_or_404(self, app, published_article):
        from flask import Flask
        with app.app_context():
            a = ArticleService.get_or_404(published_article.id)
            assert a is not None
            assert a.title == "Flask 入门指南"

    def test_get_or_404_not_found(self, app):
        from werkzeug.exceptions import NotFound
        with app.app_context():
            with pytest.raises(NotFound):
                ArticleService.get_or_404(99999)

    def test_get_published_by_slug(self, app, published_article):
        with app.app_context():
            a = ArticleService.get_published_by_slug(published_article.slug)
            assert a is not None

    def test_get_published_by_slug_draft_not_found(self, app, draft_article):
        with app.app_context():
            a = ArticleService.get_published_by_slug(draft_article.slug)
            assert a is None


# ============================================================
# CommentService Tests
# ============================================================


class TestCommentService:
    def test_validate_valid(self):
        data = {"nickname": "评论者", "email": "test@example.com", "content": "评论内容"}
        errors = CommentService.validate(data)
        assert len(errors) == 0

    def test_validate_empty_nickname(self):
        errors = CommentService.validate({"nickname": "", "email": "t@t.com", "content": "test"})
        assert any("昵称" in e for e in errors)

    def test_validate_invalid_email(self):
        errors = CommentService.validate({"nickname": "u", "email": "bad", "content": "test"})
        assert any("邮箱格式不正确" in e for e in errors)

    def test_validate_empty_content(self):
        errors = CommentService.validate({"nickname": "u", "email": "t@t.com", "content": ""})
        assert any("评论内容" in e for e in errors)

    def test_validate_long_nickname(self):
        errors = CommentService.validate({"nickname": "a" * 100, "email": "t@t.com", "content": "test"})
        assert any("80" in e for e in errors or [""])

    def test_validate_long_content(self):
        errors = CommentService.validate({"nickname": "u", "email": "t@t.com", "content": "a" * 2000})
        assert any("1000" in e for e in errors or [""])

    def test_create_pending(self, app, published_article):
        with app.app_context():
            a = Article.query.first()
            data = {"nickname": "评论者", "email": "c@test.com", "content": "好文章！"}
            comment, errors = CommentService.create_pending(a, data)
            assert len(errors) == 0
            assert comment.status == COMMENT_STATUS_PENDING

    def test_approve(self, app, published_article):
        with app.app_context():
            a = Article.query.first()
            data = {"nickname": "u", "email": "u@t.com", "content": "test"}
            comment, _ = CommentService.create_pending(a, data)
            CommentService.approve(comment)
            assert comment.status == COMMENT_STATUS_APPROVED

    def test_hide(self, app, published_article):
        with app.app_context():
            a = Article.query.first()
            data = {"nickname": "u", "email": "u@t.com", "content": "test"}
            comment, _ = CommentService.create_pending(a, data)
            CommentService.hide(comment)
            from app.models import COMMENT_STATUS_HIDDEN
            assert comment.status == COMMENT_STATUS_HIDDEN

    def test_delete(self, app, published_article):
        with app.app_context():
            a = Article.query.first()
            data = {"nickname": "u", "email": "u@t.com", "content": "test"}
            comment, _ = CommentService.create_pending(a, data)
            cid = comment.id
            CommentService.delete(comment)
            assert Comment.query.get(cid) is None

    def test_approved_for_article(self, app, published_article):
        with app.app_context():
            a = Article.query.first()
            data = {"nickname": "u", "email": "u@t.com", "content": "test"}
            c1, _ = CommentService.create_pending(a, data)
            CommentService.approve(c1)
            comments = CommentService.approved_for_article(a.id)
            assert len(comments) == 1
            assert all(c.status == COMMENT_STATUS_APPROVED for c in comments)

    def test_list_admin(self, app, published_article):
        with app.app_context():
            comments = CommentService.list_admin()
            assert isinstance(comments, list)

    def test_list_admin_filtered(self, app, published_article):
        with app.app_context():
            a = Article.query.first()
            data = {"nickname": "u", "email": "u@t.com", "content": "test"}
            CommentService.create_pending(a, data)
            comments = CommentService.list_admin(status=COMMENT_STATUS_PENDING)
            assert all(c.status == COMMENT_STATUS_PENDING for c in comments)


# ============================================================
# CategoryService Tests
# ============================================================


class TestCategoryService:
    def test_create(self, app):
        with app.app_context():
            cat, errors = CategoryService.create({
                "name": "新分类",
                "description": "描述",
                "sort_order": "10",
            })
            assert len(errors) == 0
            assert cat.name == "新分类"
            assert cat.sort_order == 10

    def test_create_duplicate(self, app, category):
        with app.app_context():
            cat, errors = CategoryService.create({"name": "技术实践"})
            assert cat is None
            assert len(errors) > 0

    def test_update(self, app, category):
        with app.app_context():
            c = Category.query.first()
            errors = CategoryService.update(c, {"name": "更新名称"})
            assert len(errors) == 0
            assert c.name == "更新名称"

    def test_delete_with_articles(self, app, category, published_article):
        with app.app_context():
            c = Category.query.first()
            errors = CategoryService.delete(c)
            assert len(errors) > 0  # Cannot delete category with articles

    def test_delete_empty(self, app):
        with app.app_context():
            cat, _ = CategoryService.create({"name": "空分类"})
            errors = CategoryService.delete(cat)
            assert len(errors) == 0

    def test_all_ordered(self, app):
        with app.app_context():
            CategoryService.create({"name": "B类", "sort_order": "2"})
            CategoryService.create({"name": "A类", "sort_order": "1"})
            categories = CategoryService.all_ordered()
            assert categories[0].name == "A类"


# ============================================================
# TagService Tests
# ============================================================


class TestTagService:
    def test_create(self, app):
        with app.app_context():
            tag, errors = TagService.create({"name": "新标签"})
            assert len(errors) == 0
            assert tag.name == "新标签"

    def test_create_duplicate(self, app, tag):
        with app.app_context():
            t, errors = TagService.create({"name": "Python"})
            assert t is None
            assert len(errors) > 0

    def test_delete(self, app):
        with app.app_context():
            t, _ = TagService.create({"name": "待删除"})
            TagService.delete(t)
            assert Tag.query.get(t.id) is None


# ============================================================
# ColumnService Tests
# ============================================================


class TestColumnService:
    def test_create(self, app, normal_user):
        with app.app_context():
            col, errors = ColumnService.create(
                {"name": "新专栏", "description": "描述"},
                normal_user,
            )
            assert len(errors) == 0
            assert col.name == "新专栏"

    def test_create_duplicate(self, app, column, normal_user):
        with app.app_context():
            col, errors = ColumnService.create(
                {"name": "Flask 实践手记"},
                normal_user,
            )
            assert col is None
            assert len(errors) > 0

    def test_delete_with_articles(self, app, column, published_article):
        with app.app_context():
            c = BlogColumn.query.first()
            c.articles.append(Article.query.first())
            db.session.commit()
            errors = ColumnService.delete(c)
            assert len(errors) > 0

    def test_by_user(self, app, column, normal_user):
        with app.app_context():
            cols = ColumnService.by_user(normal_user.id)
            assert len(cols) >= 1

    def test_all_active(self, app, column):
        with app.app_context():
            cols = ColumnService.all_active()
            assert len(cols) >= 1
            assert all(c.status == "active" for c in cols)


# ============================================================
# UserService Tests
# ============================================================


class TestUserService:
    def test_update_profile(self, app, normal_user):
        with app.app_context():
            u = UserService.get_or_404(normal_user.id)
            errors = UserService.update_profile(u, {
                "nickname": "新昵称",
                "email": "new@test.com",
                "bio": "新简介",
            })
            assert len(errors) == 0
            assert u.nickname == "新昵称"
            assert u.email == "new@test.com"

    def test_update_profile_duplicate_email(self, app, normal_user, second_user):
        with app.app_context():
            u = UserService.get_or_404(normal_user.id)
            errors = UserService.update_profile(u, {
                "nickname": "林知夏",
                "email": "bob@example.com",  # bob's email
                "bio": "test",
            })
            assert len(errors) > 0

    def test_change_password(self, app, normal_user):
        with app.app_context():
            u = UserService.get_or_404(normal_user.id)
            errors = UserService.change_password(u, {
                "old_password": "user123456",
                "new_password": "newpass123",
                "confirm_password": "newpass123",
            })
            assert len(errors) == 0
            assert u.check_password("newpass123") is True

    def test_change_password_wrong_old(self, app, normal_user):
        with app.app_context():
            u = UserService.get_or_404(normal_user.id)
            errors = UserService.change_password(u, {
                "old_password": "wrong",
                "new_password": "newpass",
                "confirm_password": "newpass",
            })
            assert len(errors) > 0

    def test_change_password_mismatch(self, app, normal_user):
        with app.app_context():
            u = UserService.get_or_404(normal_user.id)
            errors = UserService.change_password(u, {
                "old_password": "user123456",
                "new_password": "newpass1",
                "confirm_password": "newpass2",
            })
            assert len(errors) > 0

    def test_set_status(self, app, normal_user):
        with app.app_context():
            u = UserService.get_or_404(normal_user.id)
            UserService.set_status(u, "disabled")
            assert u.status == "disabled"
            UserService.set_status(u, "active")
            assert u.status == "active"

    def test_all_users(self, app, normal_user, admin_user):
        with app.app_context():
            users = UserService.all_users()
            assert len(users) >= 2

    def test_interaction_summary(self, app, normal_user):
        with app.app_context():
            summary = UserService.interaction_summary(normal_user)
            assert "comments" in summary
            assert "likes" in summary
            assert "favorites" in summary


# ============================================================
# DashboardService Tests
# ============================================================


class TestDashboardService:
    def test_stats(self, app, admin_user, category, published_article):
        with app.app_context():
            stats = DashboardService.stats()
            assert "article_count" in stats
            assert "user_count" in stats
            assert "category_count" in stats
            assert isinstance(stats["article_count"], int)
            assert isinstance(stats["user_count"], int)
