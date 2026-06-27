from datetime import datetime

from sqlalchemy import or_

from app.extensions import db
from app.models import (
    ARTICLE_STATUS_DRAFT,
    ARTICLE_STATUS_PUBLISHED,
    ARTICLE_STATUSES,
    Article,
    Category,
    Comment,
    Tag,
)
from app.services import make_slug, normalize_text


class ArticleService:
    @staticmethod
    def list_admin_articles():
        return Article.query.order_by(Article.updated_at.desc()).all()

    @staticmethod
    def list_published(page=1, per_page=6):
        return (
            Article.query.filter_by(status=ARTICLE_STATUS_PUBLISHED)
            .order_by(Article.published_at.desc(), Article.created_at.desc())
            .paginate(page=page, per_page=per_page, error_out=False)
        )

    @staticmethod
    def search_published(keyword, page=1, per_page=6):
        keyword = normalize_text(keyword)
        query = Article.query.filter_by(status=ARTICLE_STATUS_PUBLISHED)
        if keyword:
            like = f"%{keyword}%"
            query = query.filter(
                or_(
                    Article.title.ilike(like),
                    Article.summary.ilike(like),
                    Article.content.ilike(like),
                )
            )
        return (
            query.order_by(Article.published_at.desc(), Article.created_at.desc())
            .paginate(page=page, per_page=per_page, error_out=False)
        )

    @staticmethod
    def by_category(category_id, page=1, per_page=6):
        return (
            Article.query.filter_by(
                category_id=category_id,
                status=ARTICLE_STATUS_PUBLISHED,
            )
            .order_by(Article.published_at.desc(), Article.created_at.desc())
            .paginate(page=page, per_page=per_page, error_out=False)
        )

    @staticmethod
    def by_tag(tag_id, page=1, per_page=6):
        return (
            Article.query.filter(Article.tags.any(Tag.id == tag_id))
            .filter_by(status=ARTICLE_STATUS_PUBLISHED)
            .order_by(Article.published_at.desc(), Article.created_at.desc())
            .paginate(page=page, per_page=per_page, error_out=False)
        )

    @staticmethod
    def get_published_by_slug(slug):
        return Article.query.filter_by(
            slug=slug,
            status=ARTICLE_STATUS_PUBLISHED,
        ).first()

    @staticmethod
    def get_or_404(article_id):
        return Article.query.get_or_404(article_id)

    @staticmethod
    def validate(data):
        errors = []
        title = normalize_text(data.get("title"))
        summary = normalize_text(data.get("summary"))
        content = normalize_text(data.get("content"))
        status = normalize_text(data.get("status")) or ARTICLE_STATUS_DRAFT
        category_id = data.get("category_id")

        if not title:
            errors.append("文章标题不能为空。")
        if len(title) > 160:
            errors.append("文章标题不能超过 160 个字符。")
        if len(summary) > 500:
            errors.append("文章摘要不能超过 500 个字符。")
        if not content:
            errors.append("文章正文不能为空。")
        if status not in ARTICLE_STATUSES:
            errors.append("文章状态不正确。")
        if not category_id:
            errors.append("请选择文章分类。")
        elif not Category.query.get(category_id):
            errors.append("选择的分类不存在。")

        return errors

    @staticmethod
    def create(data, tag_ids):
        errors = ArticleService.validate(data)
        if errors:
            return None, errors

        status = data.get("status") or ARTICLE_STATUS_DRAFT
        article = Article(
            title=normalize_text(data.get("title")),
            slug=ArticleService.unique_slug(data.get("title")),
            summary=normalize_text(data.get("summary")),
            content=normalize_text(data.get("content")),
            status=status,
            category_id=int(data.get("category_id")),
            author=normalize_text(data.get("author")) or "管理员",
            published_at=datetime.utcnow() if status == ARTICLE_STATUS_PUBLISHED else None,
        )
        article.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all() if tag_ids else []
        db.session.add(article)
        db.session.commit()
        return article, []

    @staticmethod
    def update(article, data, tag_ids):
        errors = ArticleService.validate(data)
        if errors:
            return errors

        old_status = article.status
        status = data.get("status") or ARTICLE_STATUS_DRAFT
        article.title = normalize_text(data.get("title"))
        article.summary = normalize_text(data.get("summary"))
        article.content = normalize_text(data.get("content"))
        article.status = status
        article.category_id = int(data.get("category_id"))
        article.author = normalize_text(data.get("author")) or "管理员"
        if old_status != ARTICLE_STATUS_PUBLISHED and status == ARTICLE_STATUS_PUBLISHED:
            article.published_at = datetime.utcnow()
        if status == ARTICLE_STATUS_DRAFT:
            article.published_at = None
        article.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all() if tag_ids else []
        db.session.commit()
        return []

    @staticmethod
    def delete(article):
        db.session.delete(article)
        db.session.commit()

    @staticmethod
    def increment_view(article):
        article.view_count += 1
        db.session.commit()

    @staticmethod
    def unique_slug(title, article_id=None):
        base = make_slug(title)
        slug = base
        index = 2
        while True:
            query = Article.query.filter_by(slug=slug)
            if article_id:
                query = query.filter(Article.id != article_id)
            if not query.first():
                return slug
            slug = f"{base}-{index}"
            index += 1

    @staticmethod
    def admin_comment_count(article):
        return Comment.query.filter_by(article_id=article.id).count()
