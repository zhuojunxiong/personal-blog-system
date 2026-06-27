from flask import Blueprint, abort, render_template, request
from flask_login import current_user

from app.article.services import ArticleService
from app.category.services import CategoryService
from app.column.services import ColumnService
from app.comment.services import CommentService
from app.models import COMMENT_STATUS_APPROVED, Article, BlogColumn, Comment, User
from app.tag.services import TagService

public_bp = Blueprint("public", __name__)


@public_bp.route("/")
def index():
    page = request.args.get("page", 1, type=int)
    pagination = ArticleService.list_published(page=page)
    return render_template(
        "public/index.html",
        pagination=pagination,
        articles=pagination.items,
        categories=CategoryService.all_ordered(),
        tags=TagService.all_ordered(),
        columns=ColumnService.all_active()[:6],
        active_authors=User.query.filter_by(role="user", status="active").limit(6).all(),
        latest_comments=Comment.query.filter_by(status=COMMENT_STATUS_APPROVED).order_by(Comment.created_at.desc()).limit(5).all(),
    )


@public_bp.route("/articles/<slug>")
def article_detail(slug):
    article = ArticleService.get_published_by_slug(slug)
    if not article:
        abort(404)
    ArticleService.increment_view(article)
    comments = CommentService.approved_for_article(article.id)
    return render_template(
        "public/article_detail.html",
        article=article,
        comments=comments,
        liked=ArticleService.liked_by(article, current_user),
        favorited=ArticleService.favorited_by(article, current_user),
    )


@public_bp.route("/categories")
def category_list():
    categories = CategoryService.all_ordered()
    return render_template("public/categories.html", categories=categories)


@public_bp.route("/categories/<int:category_id>")
def category_detail(category_id):
    category = CategoryService.get_or_404(category_id)
    page = request.args.get("page", 1, type=int)
    pagination = ArticleService.by_category(category.id, page=page)
    return render_template(
        "public/category_detail.html",
        category=category,
        pagination=pagination,
        articles=pagination.items,
    )


@public_bp.route("/tags")
def tag_list():
    tags = TagService.all_ordered()
    return render_template("public/tags.html", tags=tags)


@public_bp.route("/tags/<int:tag_id>")
def tag_detail(tag_id):
    tag = TagService.get_or_404(tag_id)
    page = request.args.get("page", 1, type=int)
    pagination = ArticleService.by_tag(tag.id, page=page)
    return render_template(
        "public/tag_detail.html",
        tag=tag,
        pagination=pagination,
        articles=pagination.items,
    )


@public_bp.route("/search")
def search():
    keyword = request.args.get("q", "").strip()
    page = request.args.get("page", 1, type=int)
    pagination = ArticleService.search_published(keyword, page=page)
    return render_template(
        "public/search.html",
        keyword=keyword,
        pagination=pagination,
        articles=pagination.items,
    )


@public_bp.route("/articles")
def articles():
    page = request.args.get("page", 1, type=int)
    pagination = ArticleService.list_published(page=page)
    return render_template(
        "public/articles.html",
        pagination=pagination,
        articles=pagination.items,
    )
