from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.admin.decorators import admin_required
from app.ai.services import AIServiceError, ai_service
from app.article.services import ArticleService
from app.extensions import csrf, db
from app.models import AiLog

ai_bp = Blueprint("ai", __name__)


@ai_bp.route("/admin/ai")
@admin_required
def index():
    return render_template(
        "admin/ai/index.html",
        status_message=ai_service.provider_status(),
        is_configured=ai_service.is_configured(),
    )


# DEPRECATED: placeholder route, retained for backward compatibility
@ai_bp.route("/admin/ai/placeholder", methods=["POST"])
@admin_required
def placeholder():
    flash(ai_service.provider_status(), "info")
    return redirect(request.referrer or url_for("ai.index"))


@ai_bp.route("/ai/status")
@login_required
def status():
    return jsonify(
        {
            "ok": ai_service.is_configured(),
            "message": ai_service.provider_status(),
        }
    )


@ai_bp.route("/ai/summary", methods=["POST"])
@csrf.exempt
@login_required
def summary():
    data = _request_data()
    content = data.get("content", "")
    article = _get_accessible_article(data.get("article_id"))
    return _run_ai("summary", content, article, lambda: ai_service.generate_summary(content))


@ai_bp.route("/ai/tags", methods=["POST"])
@csrf.exempt
@login_required
def tags():
    data = _request_data()
    content = data.get("content", "")
    article = _get_accessible_article(data.get("article_id"))
    return _run_ai("tags", content, article, lambda: ai_service.recommend_tags(content))


@ai_bp.route("/ai/research", methods=["POST"])
@csrf.exempt
@login_required
def research():
    data = _request_data()
    query = data.get("query") or data.get("question") or data.get("content") or ""
    return _run_ai("research", query, None, lambda: ai_service.research_online(query))


@ai_bp.route("/ai/search-summary", methods=["POST"])
@csrf.exempt
@login_required
def search_summary():
    data = _request_data()
    title = data.get("title", "")
    summary_text = data.get("summary", "")
    content = data.get("content", "")
    article = _get_accessible_article(data.get("article_id"))
    input_text = f"标题：{title}\n\n摘要：{summary_text}\n\n正文：\n{content}"
    return _run_ai(
        "search_summary",
        input_text,
        article,
        lambda: ai_service.generate_search_summary(title, summary_text, content),
    )


@ai_bp.route("/ai/polish", methods=["POST"])
@csrf.exempt
@login_required
def polish():
    data = _request_data()
    content = data.get("content", "")
    article = _get_accessible_article(data.get("article_id"))
    return _run_ai("polish", content, article, lambda: ai_service.polish_article(content))


@ai_bp.route("/ai/chat", methods=["POST"])
@csrf.exempt
@login_required
def chat():
    data = _request_data()
    question = data.get("question", "")
    article = _get_accessible_article(data.get("article_id"))
    content = data.get("content", "")
    if article and not content:
        content = article.content
    input_text = f"文章：\n{content}\n\n问题：\n{question}"
    return _run_ai("chat", input_text, article, lambda: ai_service.chat_with_article(content, question))


@ai_bp.route("/ai/outline", methods=["POST"])
@csrf.exempt
@login_required
def outline():
    data = _request_data()
    content = data.get("content", "")
    article = _get_accessible_article(data.get("article_id"))
    return _run_ai("outline", content, article, lambda: ai_service.generate_outline(content))


@ai_bp.route("/ai/titles", methods=["POST"])
@csrf.exempt
@login_required
def suggest_titles():
    data = _request_data()
    content = data.get("content", "")
    article = _get_accessible_article(data.get("article_id"))
    return _run_ai("title", content, article, lambda: ai_service.suggest_titles(content))


@ai_bp.route("/ai/search", methods=["POST"])
# CSRF exempt: this is a public read-only search endpoint. Rate limiting should be considered for production.
@csrf.exempt
def smart_search():
    """AI 智能搜索 JSON API（公开端点）。
    请求体: {query: str, page: int(1), page_size: int(5)}
    响应: {ok: bool, understanding: str, results: [...], total: int, fallback: bool}
    """
    data = _request_data()
    query = (data.get("query") or data.get("q") or "").strip()
    if not query:
        return jsonify({"ok": False, "message": "请输入搜索内容。"}), 400

    page = max(1, int(data.get("page") or 1))
    page_size = min(max(1, int(data.get("page_size") or data.get("pageSize") or 5)), 20)

    try:
        result = ai_service.smart_search(query, page=page, per_page=page_size)
    except AIServiceError as exc:
        _log("smart_search", query, str(exc))
        return jsonify({"ok": False, "message": str(exc)}), 503

    _log(
        "smart_search",
        query,
        f"理解: {result.get('understanding', '')}; "
        f"结果数: {result.get('total', 0)}; "
        f"降级: {result.get('fallback', False)}",
    )
    return jsonify(
        {
            "ok": True,
            "understanding": result.get("understanding", ""),
            "results": result.get("results", []),
            "total": result.get("total", 0),
            "fallback": result.get("fallback", False),
        }
    )


def _request_data():
    if request.is_json:
        return request.get_json(silent=True) or {}
    return request.form


def _get_accessible_article(article_id):
    if not article_id:
        return None
    try:
        article_id = int(article_id)
    except (TypeError, ValueError):
        return None
    article = ArticleService.get_or_404(article_id)
    if article.user_id == current_user.id or current_user.is_admin:
        return article
    return None


def _run_ai(scene, input_text, article, callback):
    try:
        output = callback()
    except AIServiceError as exc:
        _log(scene, input_text, str(exc), article)
        return jsonify({"ok": False, "message": str(exc)}), 503

    _log(scene, input_text, output if isinstance(output, str) else ", ".join(output), article)
    return jsonify({"ok": True, "result": output})


def _log(scene, input_text, output, article=None):
    db.session.add(
        AiLog(
            article_id=article.id if article else None,
            scene=scene,
            input_text=input_text or "",
            ai_output=output or "",
        )
    )
    db.session.commit()
