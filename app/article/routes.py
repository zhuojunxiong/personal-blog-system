from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required

from app.admin.decorators import admin_required
from app.article.services import ArticleService
from app.category.services import CategoryService
from app.column.services import ColumnService
from app.models import ARTICLE_STATUS_DRAFT, ARTICLE_STATUS_PUBLISHED
from app.services import parse_int_list
from app.tag.services import TagService

article_bp = Blueprint("article", __name__, url_prefix="/admin/articles")


@article_bp.route("/")
@admin_required
def index():
    return render_template(
        "admin/articles/index.html",
        articles=ArticleService.list_admin_articles(),
    )


@article_bp.route("/new", methods=["GET", "POST"])
@admin_required
def create():
    categories = CategoryService.all_ordered()
    tags = TagService.all_ordered()
    columns = ColumnService.all_active()
    if request.method == "POST":
        article, errors = ArticleService.create(
            request.form,
            parse_int_list(request.form.getlist("tag_ids")),
        )
        if not errors:
            flash("文章创建成功。", "success")
            return redirect(url_for("article.index"))
        for error in errors:
            flash(error, "danger")
    return render_template(
        "admin/articles/form.html",
        article=None,
        categories=categories,
        tags=tags,
        columns=columns,
        status_draft=ARTICLE_STATUS_DRAFT,
        status_published=ARTICLE_STATUS_PUBLISHED,
    )


@article_bp.route("/<int:article_id>/edit", methods=["GET", "POST"])
@admin_required
def edit(article_id):
    article = ArticleService.get_or_404(article_id)
    categories = CategoryService.all_ordered()
    tags = TagService.all_ordered()
    columns = ColumnService.all_active()
    if request.method == "POST":
        errors = ArticleService.update(
            article,
            request.form,
            parse_int_list(request.form.getlist("tag_ids")),
        )
        if not errors:
            flash("文章更新成功。", "success")
            return redirect(url_for("article.index"))
        for error in errors:
            flash(error, "danger")
    return render_template(
        "admin/articles/form.html",
        article=article,
        categories=categories,
        tags=tags,
        columns=columns,
        status_draft=ARTICLE_STATUS_DRAFT,
        status_published=ARTICLE_STATUS_PUBLISHED,
    )


@article_bp.route("/<int:article_id>/delete", methods=["POST"])
@admin_required
def delete(article_id):
    article = ArticleService.get_or_404(article_id)
    ArticleService.delete(article)
    flash("文章已删除。", "success")
    return redirect(url_for("article.index"))

