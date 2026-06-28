from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy.exc import SQLAlchemyError

from app.admin.decorators import admin_required
from app.article.services import ArticleService
from app.category.services import CategoryService
from app.column.services import ColumnService
from app.extensions import db
from app.models import (
    ARTICLE_STATUS_DRAFT,
    ARTICLE_STATUS_PUBLISHED,
    COMMENT_STATUS_APPROVED,
    COMMENT_STATUS_PENDING,
    Article,
    Comment,
    Favorite,
)
from app.services import parse_int_list
from app.tag.services import TagService
from app.user.services import UserService

user_bp = Blueprint("user", __name__)


@user_bp.route("/users/<int:user_id>")
def profile(user_id):
    user = UserService.get_or_404(user_id)
    return render_template(
        "public/user_profile.html",
        profile_user=user,
        columns=ColumnService.by_user(user.id),
        articles=ArticleService.published_by_user(user.id),
    )


@user_bp.route("/profile")
@login_required
def profile_home():
    context = _personal_space_context()
    return render_template("user/profile.html", **context)


@user_bp.route("/me")
@login_required
def center():
    return redirect(url_for("user.profile_home"))


@user_bp.route("/profile/archive")
@login_required
def archive():
    context = _personal_space_context()
    return render_template("user/archive.html", **context)


@user_bp.route("/profile/reading")
@login_required
def reading():
    context = _personal_space_context()
    return render_template("user/reading.html", **context)


@user_bp.route("/talk")
@login_required
def talk():
    selected_article = None
    selected_slug = request.args.get("article", "").strip()
    if selected_slug:
        selected_article = ArticleService.get_published_by_slug(selected_slug)
    received_comments = (
        Comment.query.join(Article)
        .filter(Article.user_id == current_user.id)
        .order_by(Comment.created_at.desc())
        .all()
    )
    my_comments = Comment.query.filter_by(user_id=current_user.id).order_by(Comment.created_at.desc()).all()
    pending_comments = [comment for comment in received_comments if comment.status == COMMENT_STATUS_PENDING]
    approved_comments = [comment for comment in received_comments if comment.status == COMMENT_STATUS_APPROVED]
    recent_exchanges = sorted(
        received_comments[:5] + my_comments[:5],
        key=lambda comment: comment.created_at,
        reverse=True,
    )[:8]
    return render_template(
        "user/talk.html",
        received_comments=received_comments,
        my_comments=my_comments,
        pending_comments=pending_comments,
        approved_comments=approved_comments,
        recent_exchanges=recent_exchanges,
        selected_article=selected_article,
    )


@user_bp.route("/settings")
@login_required
def settings():
    return render_template("user/settings.html")


@user_bp.route("/settings/password", methods=["POST"])
@login_required
def change_password():
    errors = UserService.change_password(current_user, request.form)
    if errors:
        for error in errors:
            flash(error, "danger")
    else:
        flash("密码已更新。", "success")
    return redirect(url_for("user.settings"))


@user_bp.route("/me/profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    if request.method == "POST":
        errors = UserService.update_profile(current_user, request.form)
        if not errors:
            flash("个人资料已更新。", "success")
            return redirect(url_for("user.center"))
        for error in errors:
            flash(error, "danger")
    return render_template("user/profile_form.html")


@user_bp.route("/write", methods=["GET", "POST"])
@login_required
def write_article():
    return _write_article_form()


@user_bp.route("/write/<int:article_id>", methods=["GET", "POST"])
@login_required
def edit_article_alias(article_id):
    return _write_article_form(ArticleService.get_or_404(article_id))


@user_bp.route("/my/articles/<int:article_id>/edit", methods=["GET", "POST"])
@login_required
def edit_article(article_id):
    return _write_article_form(ArticleService.get_or_404(article_id))


def _write_article_form(article=None):
    if article and article.user_id != current_user.id and not current_user.is_admin:
        abort(403)
    categories = CategoryService.all_ordered()
    tags = TagService.all_ordered()
    columns = ColumnService.by_user(current_user.id)
    if request.method == "POST":
        status = request.form.get("status") or ARTICLE_STATUS_DRAFT
        try:
            if article:
                errors = ArticleService.update(article, request.form, parse_int_list(request.form.getlist("tag_ids")))
            else:
                article, errors = ArticleService.create(
                    request.form,
                    parse_int_list(request.form.getlist("tag_ids")),
                    user=current_user,
                )
        except SQLAlchemyError:
            db.session.rollback()
            errors = ["文章保存失败，请稍后重试。"]
        if not errors:
            if status == ARTICLE_STATUS_PUBLISHED:
                flash("文章已发布。", "success")
                return redirect(url_for("public.article_detail", slug=article.slug))
            flash("草稿已保存。", "success")
            return redirect(url_for("user.edit_article_alias", article_id=article.id, saved=1))
        for error in errors:
            flash(error, "danger")
    return render_template(
        "user/write.html",
        article=article,
        categories=categories,
        tags=tags,
        columns=columns,
        status_draft=ARTICLE_STATUS_DRAFT,
        status_published=ARTICLE_STATUS_PUBLISHED,
    )


@user_bp.route("/my/articles/<int:article_id>/delete", methods=["POST"])
@login_required
def delete_article(article_id):
    article = ArticleService.get_or_404(article_id)
    if article.user_id != current_user.id and not current_user.is_admin:
        abort(403)
    ArticleService.delete(article)
    flash("文章已删除。", "success")
    return redirect(url_for("user.center"))


@user_bp.route("/admin/users")
@admin_required
def admin_users():
    return render_template("admin/users/index.html", users=UserService.all_users())


@user_bp.route("/admin/users/<int:user_id>/toggle", methods=["POST"])
@admin_required
def admin_toggle_user(user_id):
    user = UserService.get_or_404(user_id)
    if user.is_admin:
        flash("不能禁用管理员账号。", "danger")
    else:
        UserService.set_status(user, "disabled" if user.status == "active" else "active")
        flash("用户状态已更新。", "success")
    return redirect(url_for("user.admin_users"))


def _personal_space_context():
    articles = ArticleService.list_by_user(current_user.id)
    columns = ColumnService.by_user(current_user.id)
    drafts = [article for article in articles if article.status == ARTICLE_STATUS_DRAFT]
    published_articles = [article for article in articles if article.status == ARTICLE_STATUS_PUBLISHED]
    latest_draft = drafts[0] if drafts else None
    favorites = (
        Favorite.query.filter_by(user_id=current_user.id)
        .order_by(Favorite.created_at.desc())
        .all()
    )
    # TODO: 后续版本接入 ReadingHistory 后，这里改为真实最近阅读。
    recent_reads = favorites[:5]
    received_comments = (
        Comment.query.join(Article)
        .filter(Article.user_id == current_user.id)
        .order_by(Comment.created_at.desc())
        .limit(5)
        .all()
    )
    return {
        "articles": articles,
        "columns": columns,
        "drafts": drafts,
        "published_articles": published_articles,
        "latest_draft": latest_draft,
        "favorites": favorites,
        "recent_reads": recent_reads,
        "received_comments": received_comments,
    }
