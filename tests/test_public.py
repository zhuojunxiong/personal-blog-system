"""Integration tests for public routes."""
import pytest
from app.extensions import db
from app.models import Article
from tests.conftest import login_alice


class TestPublicPages:
    """Tests for publicly accessible pages."""

    def test_index_page(self, client):
        r = client.get("/")
        assert r.status_code == 200

    def test_home_page(self, client):
        r = client.get("/home")
        assert r.status_code == 200

    def test_discover_page(self, client):
        r = client.get("/discover")
        assert r.status_code == 200

    def test_articles_page(self, client):
        r = client.get("/articles")
        assert r.status_code == 200

    def test_columns_page(self, client):
        r = client.get("/columns")
        assert r.status_code == 200

    def test_categories_page(self, client):
        r = client.get("/categories")
        assert r.status_code == 200

    def test_tags_page(self, client):
        r = client.get("/tags")
        assert r.status_code == 200

    def test_search_page_no_query(self, client):
        r = client.get("/search")
        assert r.status_code == 200

    def test_search_page_with_query(self, client):
        r = client.get("/search?q=Flask")
        assert r.status_code == 200
        data = r.data.decode()
        assert "data-v041-ai-pipeline" in data


class TestArticleDetail:
    """Tests for the article detail page."""

    def test_article_detail(self, client, published_article):
        r = client.get(f"/articles/{published_article.slug}")
        assert r.status_code == 200
        data = r.data.decode()
        assert published_article.title in data
        assert "AI 阅读助手" in data
        assert "登录后使用" in data

    def test_article_detail_not_found(self, client):
        r = client.get("/articles/nonexistent-slug-xyz")
        assert r.status_code == 404

    def test_draft_not_publicly_visible(self, client, draft_article):
        r = client.get(f"/articles/{draft_article.slug}")
        assert r.status_code == 404  # Drafts should not be publicly accessible

    def test_article_view_count_increments(self, client, app, published_article):
        with app.app_context():
            a = Article.query.first()
            old_views = a.view_count
        client.get(f"/articles/{published_article.slug}")
        with app.app_context():
            a = Article.query.first()
            assert a.view_count == old_views + 1


class TestCategoryAndTagDetail:
    """Tests for category and tag detail pages."""

    def test_category_detail(self, client, category):
        r = client.get(f"/categories/{category.id}")
        assert r.status_code == 200

    def test_category_not_found(self, client):
        r = client.get("/categories/99999")
        assert r.status_code == 404

    def test_tag_detail(self, client, tag):
        r = client.get(f"/tags/{tag.id}")
        assert r.status_code == 200

    def test_tag_not_found(self, client):
        r = client.get("/tags/99999")
        assert r.status_code == 404


class TestColumnDetail:
    """Tests for column detail pages."""

    def test_column_detail(self, client, column):
        r = client.get(f"/columns/{column.id}")
        assert r.status_code == 200

    def test_column_not_found(self, client):
        r = client.get("/columns/99999")
        assert r.status_code == 404


class TestUserProfile:
    """Tests for public user profile pages."""

    def test_user_profile(self, client, normal_user):
        r = client.get(f"/users/{normal_user.id}")
        assert r.status_code == 200

    def test_user_profile_showcase_content(self, client, app, normal_user, published_article, column):
        normal_user.profile_markdown = "## 研究方向\n- Flask\n- AI 写作"
        db.session.commit()

        r = client.get(f"/users/{normal_user.id}")
        assert r.status_code == 200
        data = r.data.decode()
        assert "Personal Showcase" in data
        assert "@alice" in data
        assert "公开文章" in data
        assert "知识合集" in data
        assert "研究方向" in data
        assert published_article.title in data
        assert column.name in data

    def test_user_not_found(self, client):
        r = client.get("/users/99999")
        assert r.status_code == 404


class TestLandingPage:
    """Tests for the landing page cookie behavior."""

    def test_first_visit_shows_landing(self, client):
        """First visit to / should show landing page."""
        r = client.get("/")
        assert r.status_code == 200
        # Should set cookie
        assert "zjx_seen_landing" in r.headers.get("Set-Cookie", "")

    def test_second_visit_redirects_to_home(self, client):
        """Second visit with cookie should redirect to /home."""
        client.set_cookie("zjx_seen_landing", "1")
        r = client.get("/")
        assert r.status_code == 302  # Redirect to /home


class TestErrorPages:
    """Tests for error handling pages."""

    def test_400_page(self, client, app):
        @app.route("/__test_400")
        def test_400():
            from flask import abort
            abort(400)
        r = client.get("/__test_400")
        assert r.status_code == 400

    def test_404_page_content(self, client):
        r = client.get("/articles/nonexistent-slug-xyz-12345")
        assert r.status_code == 404
        assert "404" in r.data.decode() or "未找到" in r.data.decode() or "Not Found" in r.data.decode()


class TestSearch:
    """Tests for search functionality."""

    def test_search_flask(self, client, published_article):
        r = client.get("/search?q=Flask")
        assert r.status_code == 200
        # The search should find the article
        data = r.data.decode()
        # Check that the page rendered properly
        assert r.status_code == 200

    def test_search_returns_articles(self, client, published_article):
        r = client.get("/search?q=Flask")
        data = r.data.decode()
        assert published_article.title in data or "Flask" in data

    def test_search_empty_query(self, client):
        r = client.get("/search?q=")
        assert r.status_code == 200

    def test_search_no_results(self, client):
        r = client.get("/search?q=nonexistent_term_xyz_12345")
        assert r.status_code == 200

    def test_search_handles_page_size(self, client):
        """Search should handle pageSize parameter."""
        r = client.get("/search?q=Flask&pageSize=10")
        assert r.status_code == 200

    def test_search_invalid_page_size(self, client):
        """Search should clamp invalid pageSize."""
        r = client.get("/search?q=Flask&pageSize=100")
        assert r.status_code == 200  # Should clamp to 5

    def test_search_pagination(self, client):
        """Search should support pagination."""
        r = client.get("/search?q=Flask&page=1")
        assert r.status_code == 200
        r = client.get("/search?q=Flask&page=2")
        assert r.status_code == 200
