from math import ceil

from flask import Blueprint, abort, render_template, request, url_for
from flask_login import current_user
from sqlalchemy import or_
from sqlalchemy.exc import SQLAlchemyError

from app.article.services import ArticleService
from app.category.services import CategoryService
from app.column.services import ColumnService
from app.extensions import db
from app.models import COMMENT_STATUS_APPROVED, Article, BlogColumn, Comment, User
from app.tag.services import TagService

public_bp = Blueprint("public", __name__)


@public_bp.route("/")
def index():
    return render_template("v041/landing.html")


@public_bp.route("/home")
def home():
    return render_template("v041/home.html")


@public_bp.route("/discover")
def discover():
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
    try:
        ArticleService.increment_view(article)
    except SQLAlchemyError:
        db.session.rollback()
    content_lines = [line.strip() for line in article.content.splitlines() if line.strip()]
    content_blocks = []
    toc_items = []
    heading_index = 0
    for line in content_lines:
        is_heading = (
            len(line) <= 32
            and (
                line.startswith(("#", "一、", "二、", "三、", "四、", "五、", "六、"))
                or line.endswith(("：", ":"))
            )
        )
        text = line.lstrip("#").strip() if line.startswith("#") else line
        if is_heading:
            heading_index += 1
            toc_items.append(text.rstrip("：:"))
            content_blocks.append({"is_heading": True, "index": heading_index, "text": text.rstrip("：:")})
        else:
            content_blocks.append({"is_heading": False, "index": None, "text": text})
    word_count = len(article.content)
    reading_minutes = max(1, ceil(word_count / 450))
    referrer = request.referrer or ""
    back_url = referrer if "/search" in referrer else url_for("public.home")
    return render_template(
        "v041/article_reading.html",
        article=article,
        favorited=ArticleService.favorited_by(article, current_user),
        content_blocks=content_blocks,
        toc_items=toc_items[:6],
        word_count=word_count,
        reading_minutes=reading_minutes,
        back_url=back_url,
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
    page_size = request.args.get("pageSize", 5, type=int)
    if page_size < 1 or page_size > 20:
        page_size = 5
    pagination = ArticleService.search_published(keyword, page=page, per_page=page_size)
    columns = []
    users = []
    if keyword:
        like = f"%{keyword}%"
        columns = (
            BlogColumn.query.filter_by(status="active")
            .filter(
                or_(
                    BlogColumn.name.ilike(like),
                    BlogColumn.description.ilike(like),
                    BlogColumn.user.has(User.nickname.ilike(like)),
                    BlogColumn.user.has(User.username.ilike(like)),
                )
            )
            .limit(6)
            .all()
        )
        users = (
            User.query.filter_by(role="user", status="active")
            .filter(
                or_(
                    User.nickname.ilike(like),
                    User.username.ilike(like),
                    User.bio.ilike(like),
                )
            )
            .limit(6)
            .all()
        )
    def search_page_url(page_num):
        return url_for("public.search", q=keyword, page=page_num, pageSize=page_size)

    return render_template(
        "v041/search_results.html",
        keyword=keyword,
        pagination=pagination,
        articles=pagination.items,
        columns=columns,
        users=users,
        categories=CategoryService.all_ordered(),
        tags=TagService.all_ordered(),
        page_size=page_size,
        search_page_url=search_page_url,
    )


@public_bp.route("/articles")
def articles():
    page = request.args.get("page", 1, type=int)
    pagination = ArticleService.list_published(page=page)
    return render_template(
        "public/articles.html",
        pagination=pagination,
        articles=pagination.items,
        categories=CategoryService.all_ordered(),
        tags=TagService.all_ordered(),
    )
