from app.extensions import db
from app.models import ARTICLE_STATUS_PUBLISHED, Article, Tag
from app.services import normalize_text


class TagService:
    @staticmethod
    def all_ordered():
        return Tag.query.order_by(Tag.name.asc()).all()

    @staticmethod
    def get_or_404(tag_id):
        return Tag.query.get_or_404(tag_id)

    @staticmethod
    def published_article_count(tag):
        return (
            Article.query.filter(Article.tags.any(Tag.id == tag.id))
            .filter_by(status=ARTICLE_STATUS_PUBLISHED)
            .count()
        )

    @staticmethod
    def validate(data, tag_id=None):
        errors = []
        name = normalize_text(data.get("name"))
        if not name:
            errors.append("标签名称不能为空。")
        if len(name) > 80:
            errors.append("标签名称不能超过 80 个字符。")
        query = Tag.query.filter_by(name=name)
        if tag_id:
            query = query.filter(Tag.id != tag_id)
        if name and query.first():
            errors.append("标签名称已存在。")
        return errors

    @staticmethod
    def create(data):
        errors = TagService.validate(data)
        if errors:
            return None, errors
        tag = Tag(name=normalize_text(data.get("name")))
        db.session.add(tag)
        db.session.commit()
        return tag, []

    @staticmethod
    def update(tag, data):
        errors = TagService.validate(data, tag.id)
        if errors:
            return errors
        tag.name = normalize_text(data.get("name"))
        db.session.commit()
        return []

    @staticmethod
    def delete(tag):
        tag.articles = []
        db.session.delete(tag)
        db.session.commit()
