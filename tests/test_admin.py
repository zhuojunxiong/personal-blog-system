"""Integration tests for admin routes."""
import pytest
from app.extensions import db
from app.models import (
    ARTICLE_STATUS_PUBLISHED,
    Category,
    Comment,
    Tag,
    User,
)
from tests.conftest import login_admin, login_alice, logout


class TestAdminDashboard:
    """Tests for admin dashboard."""

    def test_dashboard(self, client, admin_user):
        login_admin(client)
        r = client.get("/admin/dashboard")
        assert r.status_code == 200

    def test_dashboard_stats(self, client, admin_user, category, published_article):
        login_admin(client)
        r = client.get("/admin/dashboard")
        data = r.data.decode()
        # Dashboard should render with stats
        assert r.status_code == 200

    def test_admin_index_redirects(self, client, admin_user):
        login_admin(client)
        r = client.get("/admin/", follow_redirects=True)
        assert r.status_code == 200


class TestAdminArticles:
    """Tests for admin article management."""

    def test_article_list(self, client, admin_user):
        login_admin(client)
        r = client.get("/admin/articles/")
        assert r.status_code == 200

    def test_article_list_shows_ai_review_column(self, client, admin_user, published_article):
        login_admin(client)
        r = client.get("/admin/articles/")
        data = r.data.decode()
        assert r.status_code == 200
        assert "AI 审核" in data
        assert "待审核" in data

    def test_create_article_page(self, client, admin_user, category):
        login_admin(client)
        r = client.get("/admin/articles/new")
        assert r.status_code == 200

    def test_create_article(self, client, admin_user, category):
        login_admin(client)
        r = client.post("/admin/articles/new", data={
            "title": "管理员文章",
            "summary": "管理员创建",
            "content": "管理员通过后台创建的文章内容。",
            "category_id": str(category.id),
            "status": ARTICLE_STATUS_PUBLISHED,
        }, follow_redirects=True)
        assert r.status_code == 200
        assert "文章创建成功" in r.data.decode()

    def test_edit_article_page(self, client, admin_user, published_article):
        login_admin(client)
        r = client.get(f"/admin/articles/{published_article.id}/edit")
        assert r.status_code == 200

    def test_edit_article(self, client, admin_user, published_article, category):
        login_admin(client)
        r = client.post(f"/admin/articles/{published_article.id}/edit", data={
            "title": "管理员编辑的标题",
            "summary": "管理员摘要",
            "content": "管理员编辑后的正文。",
            "category_id": str(category.id),
            "status": ARTICLE_STATUS_PUBLISHED,
        }, follow_redirects=True)
        assert r.status_code == 200
        assert "文章更新成功" in r.data.decode()

    def test_delete_article(self, client, admin_user, published_article):
        login_admin(client)
        r = client.post(f"/admin/articles/{published_article.id}/delete", follow_redirects=True)
        assert r.status_code == 200
        assert "已删除" in r.data.decode()


class TestAdminCategories:
    """Tests for admin category management."""

    def test_category_list(self, client, admin_user):
        login_admin(client)
        r = client.get("/admin/categories/")
        assert r.status_code == 200

    def test_create_category(self, client, admin_user):
        login_admin(client)
        r = client.post("/admin/categories/", data={
            "name": "新分类",
            "description": "描述",
            "sort_order": "5",
        }, follow_redirects=True)
        assert r.status_code == 200
        assert "分类创建成功" in r.data.decode()

    def test_create_duplicate_category(self, client, admin_user, category):
        login_admin(client)
        r = client.post("/admin/categories/", data={
            "name": "技术实践",
            "description": "dup",
        }, follow_redirects=True)
        assert "已存在" in r.data.decode()

    def test_delete_empty_category(self, client, admin_user, app):
        login_admin(client)
        with app.app_context():
            cat = Category(name="待删", description="temp", sort_order=99)
            db.session.add(cat)
            db.session.commit()
            cat_id = cat.id
        r = client.post(f"/admin/categories/{cat_id}/delete", follow_redirects=True)
        assert r.status_code == 200


class TestAdminTags:
    """Tests for admin tag management."""

    def test_tag_list(self, client, admin_user):
        login_admin(client)
        r = client.get("/admin/tags/")
        assert r.status_code == 200

    def test_create_tag(self, client, admin_user):
        login_admin(client)
        r = client.post("/admin/tags/", data={
            "name": "新标签",
        }, follow_redirects=True)
        assert r.status_code == 200
        assert "标签创建成功" in r.data.decode()

    def test_delete_tag(self, client, admin_user, app):
        login_admin(client)
        with app.app_context():
            t = Tag(name="待删除标签")
            db.session.add(t)
            db.session.commit()
            tid = t.id
        r = client.post(f"/admin/tags/{tid}/delete", follow_redirects=True)
        assert r.status_code == 200
        assert "已删除" in r.data.decode() or "已同步清理" in r.data.decode()


class TestAdminUsers:
    """Tests for admin user management."""

    def test_user_list(self, client, admin_user):
        login_admin(client)
        r = client.get("/admin/users")
        assert r.status_code == 200

    def test_toggle_user_status(self, client, admin_user, normal_user):
        login_admin(client)
        r = client.post(f"/admin/users/{normal_user.id}/toggle", follow_redirects=True)
        assert r.status_code == 200
        assert "已更新" in r.data.decode()
        # Toggle back
        client.post(f"/admin/users/{normal_user.id}/toggle", follow_redirects=True)

    def test_cannot_toggle_admin(self, client, admin_user):
        login_admin(client)
        r = client.post(f"/admin/users/{admin_user.id}/toggle", follow_redirects=True)
        assert "不能禁用管理员" in r.data.decode()


class TestAdminComments:
    """Tests for admin comment management."""

    def test_comment_list(self, client, admin_user):
        login_admin(client)
        r = client.get("/admin/comments")
        assert r.status_code == 200

    def test_comment_filter_by_status(self, client, admin_user):
        login_admin(client)
        r = client.get("/admin/comments?status=pending")
        assert r.status_code == 200

    def test_approve_comment(self, client, admin_user, app, published_article, normal_user):
        login_admin(client)
        # Create a pending comment
        client.post(f"/articles/{published_article.slug}/comments", data={
            "content": "待审核评论",
        })
        with app.app_context():
            comment = Comment.query.filter_by(status="pending").first()
        if comment:
            r = client.post(f"/admin/comments/{comment.id}/approve", follow_redirects=True)
            assert r.status_code == 200
            assert "审核通过" in r.data.decode()

    def test_hide_comment(self, client, admin_user, app, published_article):
        login_admin(client)
        client.post(f"/articles/{published_article.slug}/comments", data={
            "content": "要隐藏的评论",
        })
        with app.app_context():
            comment = Comment.query.filter_by(status="pending").first()
        if comment:
            r = client.post(f"/admin/comments/{comment.id}/hide", follow_redirects=True)
            assert r.status_code == 200
            assert "已隐藏" in r.data.decode()

    def test_delete_comment(self, client, admin_user, app, published_article):
        login_admin(client)
        client.post(f"/articles/{published_article.slug}/comments", data={
            "content": "要删除的评论",
        })
        with app.app_context():
            comment = Comment.query.filter_by(status="pending").first()
        if comment:
            r = client.post(f"/admin/comments/{comment.id}/delete", follow_redirects=True)
            assert r.status_code == 200
            assert "已删除" in r.data.decode()


class TestAdminColumns:
    """Tests for admin column management."""

    def test_column_list(self, client, admin_user):
        login_admin(client)
        r = client.get("/admin/columns")
        assert r.status_code == 200

    def test_toggle_column(self, client, admin_user, column):
        login_admin(client)
        r = client.post(f"/admin/columns/{column.id}/toggle", follow_redirects=True)
        assert r.status_code == 200
        assert "已更新" in r.data.decode()


class TestAdminAI:
    """Tests for admin AI status page."""

    def test_ai_page(self, client, admin_user):
        login_admin(client)
        r = client.get("/admin/ai")
        assert r.status_code == 200


class TestAdminAccessControl:
    """Tests that normal users cannot access admin routes."""

    def test_normal_user_cannot_access_any_admin(self, client, normal_user):
        login_alice(client)
        admin_urls = [
            "/admin/", "/admin/dashboard", "/admin/articles/",
            "/admin/users", "/admin/comments", "/admin/categories/",
            "/admin/tags/", "/admin/columns", "/admin/ai",
        ]
        for url in admin_urls:
            r = client.get(url)
            assert r.status_code in (302, 403), f"Expected 302 or 403 for {url}, got {r.status_code}"
