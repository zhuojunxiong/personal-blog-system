"""Tests for the AI reading assistant."""

from app.models import AiLog
from tests.conftest import login_alice


class TestAiReadingAssistant:
    def test_requires_login(self, client, published_article):
        response = client.post(
            "/ai/reading",
            json={"slug": published_article.slug, "mode": "summary"},
        )
        assert response.status_code == 302
        assert "/login" in response.headers["Location"]

    def test_missing_article_returns_404(self, client, normal_user):
        login_alice(client)
        response = client.post(
            "/ai/reading",
            json={"slug": "missing-article", "mode": "summary"},
        )
        assert response.status_code == 404
        assert response.get_json()["ok"] is False

    def test_ai_disabled_returns_readable_error_and_logs(self, client, app, normal_user, published_article):
        login_alice(client)
        response = client.post(
            "/ai/reading",
            json={"slug": published_article.slug, "mode": "summary"},
        )
        assert response.status_code == 503
        data = response.get_json()
        assert data["ok"] is False
        assert "AI 接口已关闭" in data["message"]

        with app.app_context():
            log = AiLog.query.filter_by(scene="reading_assistant").first()
            assert log is not None
            assert log.article_id == published_article.id

    def test_question_mode_requires_question(self, client, normal_user, published_article):
        login_alice(client)
        response = client.post(
            "/ai/reading",
            json={"slug": published_article.slug, "mode": "question", "question": ""},
        )
        assert response.status_code == 503
        assert "请输入想问文章的问题" in response.get_json()["message"]
