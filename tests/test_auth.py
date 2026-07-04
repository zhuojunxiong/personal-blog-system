"""Integration tests for authentication routes."""
import pytest
from app.extensions import db
from app.models import User
from tests.conftest import login_alice, login_admin, login_bob, logout


class TestRegistration:
    """Tests for the /register endpoint."""

    def test_get_register_page(self, client):
        r = client.get("/register")
        assert r.status_code == 200

    def test_register_success(self, client, app):
        r = client.post("/register", data={
            "username": "newuser",
            "email": "new@example.com",
            "password": "password123",
            "nickname": "新用户",
        }, follow_redirects=True)
        assert r.status_code == 200
        # Should redirect to profile home after registration
        assert "注册成功" in r.data.decode() or "书房" in r.data.decode()

    def test_register_duplicate_username(self, client, normal_user):
        r = client.post("/register", data={
            "username": "alice",
            "email": "other@example.com",
            "password": "password123",
        })
        assert "已存在" in r.data.decode() or "已被注册" in r.data.decode()

    def test_register_empty_username(self, client):
        r = client.post("/register", data={
            "username": "",
            "email": "test@example.com",
            "password": "password123",
        })
        assert "用户名" in r.data.decode()

    def test_register_invalid_email(self, client):
        r = client.post("/register", data={
            "username": "testuser2",
            "email": "invalid-email",
            "password": "password123",
        })
        assert "邮箱" in r.data.decode()

    def test_register_short_password(self, client):
        r = client.post("/register", data={
            "username": "testuser3",
            "email": "test3@example.com",
            "password": "123",
        })
        assert "密码" in r.data.decode()

    def test_register_already_logged_in(self, client, normal_user):
        """If already logged in, visiting register should redirect."""
        login_alice(client)
        r = client.get("/register", follow_redirects=True)
        assert r.status_code == 200
        # Should have been redirected away from register page


class TestLogin:
    """Tests for the /login endpoint."""

    def test_get_login_page(self, client):
        r = client.get("/login")
        assert r.status_code == 200

    def test_login_success(self, client, normal_user):
        r = client.post("/login", data={
            "username": "alice",
            "password": "user123456",
        }, follow_redirects=True)
        assert r.status_code == 200

    def test_login_wrong_password(self, client, normal_user):
        r = client.post("/login", data={
            "username": "alice",
            "password": "wrongpassword",
        })
        assert "用户名或密码错误" in r.data.decode() or "账号已被禁用" in r.data.decode()

    def test_login_nonexistent_user(self, client):
        r = client.post("/login", data={
            "username": "nonexistent",
            "password": "password",
        })
        assert "用户名或密码错误" in r.data.decode() or "账号已被禁用" in r.data.decode()

    def test_login_empty_username(self, client):
        r = client.post("/login", data={
            "username": "",
            "password": "password",
        })
        assert "请输入账号" in r.data.decode()

    def test_login_empty_password(self, client):
        r = client.post("/login", data={
            "username": "alice",
            "password": "",
        })
        assert "请输入密码" in r.data.decode()

    def test_login_by_email(self, client, normal_user):
        """User should be able to login with email as username."""
        r = client.post("/login", data={
            "username": "alice@example.com",
            "password": "user123456",
        }, follow_redirects=True)
        assert r.status_code == 200

    def test_login_disabled_user(self, client, app, normal_user):
        """Login should fail for disabled users."""
        with app.app_context():
            u = User.query.filter_by(username="alice").first()
            u.status = "disabled"
            db.session.commit()

        r = client.post("/login", data={
            "username": "alice",
            "password": "user123456",
        })
        assert "用户名或密码错误" in r.data.decode() or "账号已被禁用" in r.data.decode()

        # Restore
        with app.app_context():
            u = User.query.filter_by(username="alice").first()
            u.status = "active"
            db.session.commit()

    def test_login_redirect_next(self, client, normal_user):
        """Login should redirect to 'next' parameter."""
        r = client.post("/login?next=/write", data={
            "username": "alice",
            "password": "user123456",
        })
        assert r.status_code == 302
        assert "/write" in r.headers.get("Location", "")


class TestAdminLogin:
    """Tests for the /admin/login endpoint."""

    def test_admin_login_page(self, client):
        r = client.get("/admin/login")
        assert r.status_code == 200

    def test_admin_login_success(self, client, admin_user):
        r = client.post("/admin/login", data={
            "username": "admin",
            "password": "admin123456",
        }, follow_redirects=True)
        assert r.status_code == 200

    def test_normal_user_cannot_admin_login(self, client, normal_user):
        r = client.post("/admin/login", data={
            "username": "alice",
            "password": "user123456",
        })
        assert "普通用户不能登录后台" in r.data.decode()


class TestLogout:
    """Tests for the /logout endpoint."""

    def test_logout(self, client, normal_user):
        login_alice(client)
        r = client.get("/logout", follow_redirects=True)
        assert r.status_code == 200
        assert "已退出登录" in r.data.decode()

    def test_admin_logout(self, client, admin_user):
        login_admin(client)
        r = client.get("/admin/logout", follow_redirects=True)
        assert r.status_code == 200
        assert "已退出登录" in r.data.decode()


class TestAccessControl:
    """Tests for access control on protected pages."""

    def test_unauthenticated_access_write(self, client):
        r = client.get("/write", follow_redirects=True)
        assert r.status_code == 200
        # Should be redirected to login
        assert "login" in r.request.path.lower() or "登录" in r.data.decode()

    def test_unauthenticated_access_me(self, client):
        r = client.get("/me", follow_redirects=True)
        assert r.status_code == 200
        assert "login" in r.request.path.lower() or "登录" in r.data.decode()

    def test_unauthenticated_access_settings(self, client):
        r = client.get("/settings", follow_redirects=True)
        assert r.status_code == 200
        assert "login" in r.request.path.lower() or "登录" in r.data.decode()

    def test_unauthenticated_access_admin(self, client):
        r = client.get("/admin/dashboard", follow_redirects=True)
        assert r.status_code == 200
        # Should be redirected

    def test_normal_user_access_admin(self, client, normal_user):
        login_alice(client)
        r = client.get("/admin/dashboard")
        assert r.status_code == 302  # Redirect
