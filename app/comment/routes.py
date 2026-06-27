from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required

from app.article.services import ArticleService
from app.comment.services import CommentService
from app.models import COMMENT_STATUSES

comment_bp = Blueprint("comment", __name__)


@comment_bp.route("/articles/<slug>/comments", methods=["POST"])
def submit(slug):
    article = ArticleService.get_published_by_slug(slug)
    if not article:
        flash("文章不存在或尚未发布。", "danger")
        return redirect(url_for("public.index"))
    comment, errors = CommentService.create_pending(article, request.form)
    if errors:
        for error in errors:
            flash(error, "danger")
    else:
        flash("评论已提交，等待管理员审核。", "success")
    return redirect(url_for("public.article_detail", slug=article.slug))


@comment_bp.route("/admin/comments")
@login_required
def admin_index():
    status = request.args.get("status")
    if status not in COMMENT_STATUSES:
        status = None
    return render_template(
        "admin/comments/index.html",
        comments=CommentService.list_admin(status=status),
        current_status=status,
    )


@comment_bp.route("/admin/comments/<int:comment_id>/approve", methods=["POST"])
@login_required
def approve(comment_id):
    comment = CommentService.get_or_404(comment_id)
    CommentService.approve(comment)
    flash("评论已审核通过。", "success")
    return redirect(request.referrer or url_for("comment.admin_index"))


@comment_bp.route("/admin/comments/<int:comment_id>/hide", methods=["POST"])
@login_required
def hide(comment_id):
    comment = CommentService.get_or_404(comment_id)
    CommentService.hide(comment)
    flash("评论已隐藏。", "success")
    return redirect(request.referrer or url_for("comment.admin_index"))


@comment_bp.route("/admin/comments/<int:comment_id>/delete", methods=["POST"])
@login_required
def delete(comment_id):
    comment = CommentService.get_or_404(comment_id)
    CommentService.delete(comment)
    flash("评论已删除。", "success")
    return redirect(request.referrer or url_for("comment.admin_index"))
