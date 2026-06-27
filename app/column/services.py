from app.extensions import db
from app.models import BlogColumn
from app.services import normalize_text


class ColumnService:
    @staticmethod
    def all_active():
        return BlogColumn.query.filter_by(status="active").order_by(BlogColumn.created_at.desc()).all()

    @staticmethod
    def by_user(user_id):
        return BlogColumn.query.filter_by(user_id=user_id).order_by(BlogColumn.created_at.desc()).all()

    @staticmethod
    def get_or_404(column_id):
        return BlogColumn.query.get_or_404(column_id)

    @staticmethod
    def validate(data, user_id, column_id=None):
        errors = []
        name = normalize_text(data.get("name"))
        if not name:
            errors.append("专栏名称不能为空。")
        if len(name) > 120:
            errors.append("专栏名称不能超过 120 个字符。")
        query = BlogColumn.query.filter_by(user_id=user_id, name=name)
        if column_id:
            query = query.filter(BlogColumn.id != column_id)
        if name and query.first():
            errors.append("你已经创建过同名专栏。")
        return errors

    @staticmethod
    def create(data, user):
        errors = ColumnService.validate(data, user.id)
        if errors:
            return None, errors
        column = BlogColumn(
            user_id=user.id,
            name=normalize_text(data.get("name")),
            description=normalize_text(data.get("description")),
        )
        db.session.add(column)
        db.session.commit()
        return column, []

    @staticmethod
    def update(column, data):
        errors = ColumnService.validate(data, column.user_id, column.id)
        if errors:
            return errors
        column.name = normalize_text(data.get("name"))
        column.description = normalize_text(data.get("description"))
        column.status = normalize_text(data.get("status")) or "active"
        db.session.commit()
        return []

    @staticmethod
    def delete(column):
        if column.articles:
            return ["该专栏下仍有文章，不能直接删除。"]
        db.session.delete(column)
        db.session.commit()
        return []
