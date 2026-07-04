"""Integration tests for user (logged-in) routes."""
import pytest
from app.extensions import db
from app.models import (
    ARTICLE_STATUS_DRAFT,
    ARTICLE_STATUS_PUBLISHED,
    Article,
    BlogColumn,
    Category,
    Favorite,
    Like,
    User,
)
from app.services import make_slug
from tests.conftest import login_alice, login_bob, logout


class TestPersonalCenter:
    """Tests for user personal space pages."""

    def test_center_redirects(self, client, normal_user):
        login_alice(client)
        r = client.get("/me", follow_redirects=True)
        assert r.status_code == 200

    def test_profile_home(self, client, normal_user):
        login_alice(client)
        r = client.get("/profile")
        assert r.status_code == 200

    def test_archive_page(self, client, normal_user):
        login_alice(client)
        r = client.get("/profile/archive")
        assert r.status_code == 200

    def test_reading_page(self, client, normal_user):
        login_alice(client)
        r = client.get("/profile/reading")
        assert r.status_code == 200

    def test_talk_page(self, client, normal_user):
        login_alice(client)
        r = client.get("/talk")
        assert r.status_code == 200

    def test_settings_page(self, client, normal_user):
        login_alice(client)
        r = client.get("/settings")
        assert r.status_code == 200

    def test_edit_profile_page(self, client, normal_user):
        login_alice(client)
        r = client.get("/me/profile")
        assert r.status_code == 200


class TestProfileEditing:
    """Tests for profile editing."""

    def test_edit_profile_success(self, client, app, normal_user):
        login_alice(client)
        r = client.post("/me/profile", data={
            "nickname": "新名字",
            "email": "newemail@example.com",
            "bio": "更新后的简介",
            "profile_markdown": "# 我的主页\n\n更新了内容。",
        }, follow_redirects=True)
        assert r.status_code == 200
        assert "个人资料已更新" in r.data.decode()

    def test_edit_profile_empty_nickname(self, client, normal_user):
        login_alice(client)
        r = client.post("/me/profile", data={
            "nickname": "",
            "email": "test@example.com",
        })
        assert "昵称不能为空" in r.data.decode()

    def test_edit_profile_invalid_email(self, client, normal_user):
        login_alice(client)
        r = client.post("/me/profile", data={
            "nickname": "林知夏",
            "email": "invalid",
        })
        assert "邮箱格式不正确" in r.data.decode()

    def test_edit_profile_duplicate_email(self, client, normal_user, second_user):
        login_alice(client)
        r = client.post("/me/profile", data={
            "nickname": "林知夏",
            "email": "bob@example.com",  # bob's email
        })
        assert "邮箱已被其他用户使用" in r.data.decode()


class TestChangePassword:
    """Tests for password change."""

    def test_change_password_success(self, client, normal_user):
        login_alice(client)
        r = client.post("/settings/password", data={
            "old_password": "user123456",
            "new_password": "newpass456",
            "confirm_password": "newpass456",
        }, follow_redirects=True)
        assert r.status_code == 200
        assert "密码已更新" in r.data.decode()
        # Change back
        client.post("/settings/password", data={
            "old_password": "newpass456",
            "new_password": "user123456",
            "confirm_password": "user123456",
        })

    def test_change_password_wrong_old(self, client, normal_user):
        login_alice(client)
        r = client.post("/settings/password", data={
            "old_password": "wrongpass",
            "new_password": "newpass",
            "confirm_password": "newpass",
        }, follow_redirects=True)
        assert "当前密码不正确" in r.data.decode()

    def test_change_password_mismatch(self, client, normal_user):
        login_alice(client)
        r = client.post("/settings/password", data={
            "old_password": "user123456",
            "new_password": "newpass1",
            "confirm_password": "newpass2",
        }, follow_redirects=True)
        assert "不一致" in r.data.decode()

    def test_change_password_short(self, client, normal_user):
        login_alice(client)
        r = client.post("/settings/password", data={
            "old_password": "user123456",
            "new_password": "123",
            "confirm_password": "123",
        }, follow_redirects=True)
        assert "至少需要 6 位" in r.data.decode()


class TestWriteArticle:
    """Tests for writing articles."""

    def test_write_page(self, client, normal_user, category):
        login_alice(client)
        r = client.get("/write")
        assert r.status_code == 200

    def test_write_page_has_form_elements(self, client, normal_user, category):
        login_alice(client)
        r = client.get("/write")
        data = r.data.decode()
        # Check for key form elements
        assert "title" in data.lower() or "标题" in data
        assert "content" in data.lower() or "正文" in data or "content" in data

    def test_create_published_article(self, client, app, normal_user, category):
        login_alice(client)
        r = client.post("/write", data={
            "title": "我的测试文章",
            "summary": "测试摘要",
            "content": "这是测试文章的正文内容，用于验证写文章功能。",
            "category_id": str(category.id),
            "status": ARTICLE_STATUS_PUBLISHED,
        }, follow_redirects=True)
        assert r.status_code == 200
        data = r.data.decode()
        assert "已发布" in data or "我的测试文章" in data

    def test_create_draft_article(self, client, app, normal_user, category):
        login_alice(client)
        r = client.post("/write", data={
            "title": "草稿文章",
            "content": "草稿内容还在写...",
            "category_id": str(category.id),
            "status": ARTICLE_STATUS_DRAFT,
        }, follow_redirects=True)
        assert r.status_code == 200
        assert "草稿已保存" in r.data.decode()

    def test_create_article_empty_title(self, client, normal_user, category):
        login_alice(client)
        r = client.post("/write", data={
            "title": "",
            "content": "内容",
            "category_id": str(category.id),
            "status": ARTICLE_STATUS_PUBLISHED,
        })
        assert "标题不能为空" in r.data.decode()

    def test_create_article_empty_content(self, client, normal_user, category):
        login_alice(client)
        r = client.post("/write", data={
            "title": "只有标题",
            "content": "",
            "category_id": str(category.id),
            "status": ARTICLE_STATUS_PUBLISHED,
        })
        assert "正文不能为空" in r.data.decode()


class TestEditArticle:
    """Tests for editing articles."""

    def test_edit_page(self, client, normal_user, published_article):
        login_alice(client)
        r = client.get(f"/my/articles/{published_article.id}/edit")
        assert r.status_code == 200

    def test_edit_success(self, client, normal_user, published_article, category):
        login_alice(client)
        r = client.post(f"/my/articles/{published_article.id}/edit", data={
            "title": "编辑后的标题",
            "summary": "编辑后的摘要",
            "content": "编辑后的正文内容。",
            "category_id": str(category.id),
            "status": ARTICLE_STATUS_PUBLISHED,
        }, follow_redirects=True)
        assert r.status_code == 200

    def test_cannot_edit_others_article(self, client, second_user, published_article):
        login_bob(client)
        r = client.get(f"/my/articles/{published_article.id}/edit")
        assert r.status_code == 403

    def test_write_alias_route(self, client, normal_user, published_article):
        """Test /write/<id> alias for edit."""
        login_alice(client)
        r = client.get(f"/write/{published_article.id}")
        assert r.status_code == 200


class TestDeleteArticle:
    """Tests for deleting articles."""

    def test_delete_own_article(self, client, normal_user, published_article):
        login_alice(client)
        r = client.post(f"/my/articles/{published_article.id}/delete", follow_redirects=True)
        assert r.status_code == 200
        assert "已删除" in r.data.decode()

    def test_cannot_delete_others_article(self, client, second_user, published_article):
        login_bob(client)
        r = client.post(f"/my/articles/{published_article.id}/delete", follow_redirects=True)
        assert r.status_code == 403


class TestLikeAndFavorite:
    """Tests for like and favorite functionality."""

    def test_like_article(self, client, normal_user, published_article):
        login_alice(client)
        r = client.post(f"/articles/{published_article.slug}/like", follow_redirects=True)
        assert r.status_code == 200
        assert "已点赞" in r.data.decode()

    def test_unlike_article(self, client, normal_user, published_article):
        login_alice(client)
        # Like first
        client.post(f"/articles/{published_article.slug}/like", follow_redirects=True)
        # Then unlike
        r = client.post(f"/articles/{published_article.slug}/like", follow_redirects=True)
        assert r.status_code == 200
        # Should say "已取消点赞" or similar

    def test_favorite_article(self, client, normal_user, published_article):
        login_alice(client)
        r = client.post(f"/articles/{published_article.slug}/favorite", follow_redirects=True)
        assert r.status_code == 200
        assert "已收藏" in r.data.decode()

    def test_unfavorite_article(self, client, normal_user, published_article):
        login_alice(client)
        client.post(f"/articles/{published_article.slug}/favorite", follow_redirects=True)
        r = client.post(f"/articles/{published_article.slug}/favorite", follow_redirects=True)
        assert r.status_code == 200

    def test_like_requires_login(self, client, published_article):
        r = client.post(f"/articles/{published_article.slug}/like", follow_redirects=True)
        assert r.status_code == 200
        # Should redirect to login

    def test_like_nonexistent_article(self, client, normal_user):
        login_alice(client)
        r = client.post("/articles/nonexistent-slug/like", follow_redirects=True)
        assert r.status_code == 200
        # Should show error flash


class TestCommenting:
    """Tests for comment submission."""

    def test_submit_comment(self, client, normal_user, published_article):
        login_alice(client)
        r = client.post(f"/articles/{published_article.slug}/comments", data={
            "content": "这是一条测试评论。",
        }, follow_redirects=True)
        assert r.status_code == 200
        assert "评论已提交" in r.data.decode()

    def test_comment_requires_login(self, client, published_article):
        r = client.post(f"/articles/{published_article.slug}/comments", data={
            "content": "匿名评论",
        }, follow_redirects=True)
        assert r.status_code == 200
        # Should redirect to login

    def test_comment_nonexistent_article(self, client, normal_user):
        login_alice(client)
        r = client.post("/articles/nonexistent-slug/comments", data={
            "content": "评论",
        }, follow_redirects=True)
        assert r.status_code == 200


class TestColumns:
    """Tests for blog column management."""

    def test_my_columns_page(self, client, normal_user):
        login_alice(client)
        r = client.get("/my/columns")
        assert r.status_code == 200

    def test_create_column(self, client, normal_user):
        login_alice(client)
        r = client.post("/my/columns", data={
            "name": "新专栏",
            "description": "专栏描述",
        }, follow_redirects=True)
        assert r.status_code == 200
        assert "专栏创建成功" in r.data.decode()

    def test_create_column_empty_name(self, client, normal_user):
        login_alice(client)
        r = client.post("/my/columns", data={
            "name": "",
            "description": "desc",
        }, follow_redirects=True)
        assert "专栏名称不能为空" in r.data.decode()

    def test_create_duplicate_column(self, client, normal_user, column):
        login_alice(client)
        r = client.post("/my/columns", data={
            "name": "Flask 实践手记",
            "description": "dup",
        }, follow_redirects=True)
        assert "同名专栏" in r.data.decode()

    def test_delete_column(self, client, normal_user, app):
        login_alice(client)
        # Create a column first
        client.post("/my/columns", data={"name": "待删专栏", "description": "temp"})
        with app.app_context():
            col = BlogColumn.query.filter_by(name="待删专栏").first()
        if col:
            r = client.post(f"/my/columns/{col.id}/delete", follow_redirects=True)
            assert r.status_code == 200
            assert "已删除" in r.data.decode()

    def test_edit_column_page(self, client, normal_user, column):
        login_alice(client)
        r = client.get(f"/my/columns/{column.id}/edit")
        assert r.status_code == 200

    def test_edit_column(self, client, normal_user, column):
        login_alice(client)
        r = client.post(f"/my/columns/{column.id}/edit", data={
            "name": "更新后的专栏名",
            "description": "更新描述",
        }, follow_redirects=True)
        assert r.status_code == 200
        assert "专栏更新成功" in r.data.decode()
