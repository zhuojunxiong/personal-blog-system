"""Performance and stress tests for the blog system."""
import time
import pytest
from app.extensions import db
from app.models import (
    ARTICLE_STATUS_PUBLISHED,
    Article,
    Category,
    User,
)
from app.services import make_slug, utcnow
from tests.conftest import login_admin, login_alice


class TestResponseTime:
    """Tests for acceptable response times on key endpoints."""

    def test_homepage_response_time(self, client):
        """Homepage should respond quickly."""
        start = time.time()
        r = client.get("/")
        elapsed = time.time() - start
        assert r.status_code == 200
        assert elapsed < 2.0, f"Homepage took {elapsed:.2f}s"

    def test_search_response_time(self, client, published_article):
        """Search should respond quickly."""
        start = time.time()
        r = client.get("/search?q=Flask")
        elapsed = time.time() - start
        assert r.status_code == 200
        assert elapsed < 2.0, f"Search took {elapsed:.2f}s"

    def test_article_detail_response_time(self, client, published_article):
        """Article detail should respond quickly."""
        start = time.time()
        r = client.get(f"/articles/{published_article.slug}")
        elapsed = time.time() - start
        assert r.status_code == 200
        assert elapsed < 2.0, f"Article detail took {elapsed:.2f}s"

    def test_login_response_time(self, client, normal_user):
        """Login should respond quickly."""
        start = time.time()
        r = client.post("/login", data={
            "username": "alice",
            "password": "user123456",
        })
        elapsed = time.time() - start
        assert r.status_code in (200, 302)
        assert elapsed < 2.0, f"Login took {elapsed:.2f}s"

    def test_admin_dashboard_response_time(self, client, admin_user):
        """Admin dashboard should respond quickly."""
        login_admin(client)
        start = time.time()
        r = client.get("/admin/dashboard")
        elapsed = time.time() - start
        assert r.status_code == 200
        assert elapsed < 2.0, f"Dashboard took {elapsed:.2f}s"


class TestBulkOperations:
    """Tests for bulk data handling."""

    def test_create_many_articles(self, app, normal_user, category):
        """Creating many articles should not crash."""
        with app.app_context():
            for i in range(50):
                a = Article(
                    title=f"批量文章 {i}",
                    slug=make_slug(f"批量文章 {i}"),
                    content=f"文章内容 {i}",
                    category_id=category.id,
                    user_id=normal_user.id,
                    status=ARTICLE_STATUS_PUBLISHED,
                    published_at=utcnow(),
                )
                db.session.add(a)
            db.session.commit()
            count = Article.query.count()
            assert count >= 50

    def test_pagination_many_articles(self, client, app, normal_user, category):
        """Pagination should work correctly with many articles."""
        with app.app_context():
            for i in range(25):
                a = Article(
                    title=f"分页文章 {i}",
                    slug=make_slug(f"分页文章 {i}"),
                    content=f"内容 {i}",
                    category_id=category.id,
                    user_id=normal_user.id,
                    status=ARTICLE_STATUS_PUBLISHED,
                    published_at=utcnow(),
                )
                db.session.add(a)
            db.session.commit()

        # Test multiple pages
        for page in [1, 2, 3]:
            r = client.get(f"/articles?page={page}")
            assert r.status_code == 200

    def test_many_tags_on_article(self, app, published_article):
        """Article with many tags should be handled correctly."""
        from app.models import Tag
        with app.app_context():
            a = Article.query.first()
            for i in range(10):
                t = Tag(name=f"标签{i}")
                db.session.add(t)
                a.tags.append(t)
            db.session.commit()
            assert len(a.tags) == 10


class TestSearchPerformance:
    """Tests for search performance with varying data sizes."""

    def test_search_with_many_articles(self, client, app, normal_user, category):
        """Search should remain responsive with many articles."""
        with app.app_context():
            u = User.query.filter_by(username="alice").first()
            c = Category.query.first()
            for i in range(30):
                a = Article(
                    title=f"Python Flask 教程 {i}",
                    slug=make_slug(f"Python Flask 教程 {i}"),
                    content=f"这是关于 Flask 框架的第 {i} 篇教程",
                    category_id=c.id,
                    user_id=u.id,
                    status=ARTICLE_STATUS_PUBLISHED,
                    published_at=utcnow(),
                )
                db.session.add(a)
            db.session.commit()

        start = time.time()
        r = client.get("/search?q=Flask")
        elapsed = time.time() - start
        assert r.status_code == 200
        assert elapsed < 3.0, f"Search with 30 articles took {elapsed:.2f}s"


class TestConcurrentRequests:
    """Tests simulating concurrent access patterns."""

    def test_sequential_rapid_requests(self, client):
        """Multiple rapid requests should not crash the app."""
        urls = ["/", "/home", "/discover", "/articles", "/categories", "/tags"]
        for _ in range(3):
            for url in urls:
                r = client.get(url)
                assert r.status_code in (200, 302)

    def test_rapid_write_read_cycle(self, client, normal_user, category):
        """Rapid write-then-read cycle should work correctly."""
        login_alice(client)
        for i in range(5):
            # Write article
            r = client.post("/write", data={
                "title": f"快速文章 {i}",
                "content": f"快速内容 {i}",
                "category_id": str(category.id),
                "status": ARTICLE_STATUS_PUBLISHED,
            }, follow_redirects=True)
            assert r.status_code == 200


class TestMemoryDatabase:
    """Verify in-memory SQLite works correctly for testing."""

    def test_database_is_empty_initially(self, app):
        with app.app_context():
            assert User.query.count() == 0
            assert Article.query.count() == 0
            assert Category.query.count() == 0

    def test_fixtures_only_create_when_used(self, app):
        """Without fixtures, DB should be empty."""
        with app.app_context():
            assert User.query.count() == 0
