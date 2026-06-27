from app.extensions import db
from app.models import ARTICLE_STATUS_PUBLISHED, Article, Category
from app.services import normalize_text


class CategoryService:
    @staticmethod
    def all_ordered():
        return Category.query.order_by(Category.sort_order.asc(), Category.name.asc()).all()

    @staticmethod
    def get_or_404(category_id):
        return Category.query.get_or_404(category_id)

    @staticmethod
    def published_article_count(category):
        return Article.query.filter_by(
            category_id=category.id,
            status=ARTICLE_STATUS_PUBLISHED,
        ).count()

    @staticmethod
    def validate(data, category_id=None):
        errors = []
        name = normalize_text(data.get("name"))
        if not name:
            errors.append("分类名称不能为空。")
        if len(name) > 80:
            errors.append("分类名称不能超过 80 个字符。")

        query = Category.query.filter_by(name=name)
        if category_id:
            query = query.filter(Category.id != category_id)
        if name and query.first():
            errors.append("分类名称已存在。")
        return errors

    @staticmethod
    def create(data):
        errors = CategoryService.validate(data)
        if errors:
            return None, errors
        category = Category(
            name=normalize_text(data.get("name")),
            description=normalize_text(data.get("description")),
            sort_order=int(data.get("sort_order") or 0),
        )
        db.session.add(category)
        db.session.commit()
        return category, []

    @staticmethod
    def update(category, data):
        errors = CategoryService.validate(data, category.id)
        if errors:
            return errors
        category.name = normalize_text(data.get("name"))
        category.description = normalize_text(data.get("description"))
        category.sort_order = int(data.get("sort_order") or 0)
        db.session.commit()
        return []

    @staticmethod
    def delete(category):
        if category.articles:
            return ["该分类下仍有文章，不能直接删除。"]
        db.session.delete(category)
        db.session.commit()
        return []
