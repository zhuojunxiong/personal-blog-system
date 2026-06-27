import re

from app.extensions import db
from app.models import (
    COMMENT_STATUS_APPROVED,
    COMMENT_STATUS_HIDDEN,
    COMMENT_STATUS_PENDING,
    COMMENT_STATUSES,
    Comment,
)
from app.services import normalize_text

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class CommentService:
    @staticmethod
    def list_admin(status=None):
        query = Comment.query
        if status in COMMENT_STATUSES:
            query = query.filter_by(status=status)
        return query.order_by(Comment.created_at.desc()).all()

    @staticmethod
    def approved_for_article(article_id):
        return (
            Comment.query.filter_by(
                article_id=article_id,
                status=COMMENT_STATUS_APPROVED,
            )
            .order_by(Comment.created_at.asc())
            .all()
        )

    @staticmethod
    def get_or_404(comment_id):
        return Comment.query.get_or_404(comment_id)

    @staticmethod
    def validate(data):
        errors = []
        nickname = normalize_text(data.get("nickname"))
        email = normalize_text(data.get("email"))
        content = normalize_text(data.get("content"))
        if not nickname:
            errors.append("昵称不能为空。")
        if len(nickname) > 80:
            errors.append("昵称不能超过 80 个字符。")
        if not email:
            errors.append("邮箱不能为空。")
        elif not EMAIL_PATTERN.match(email):
            errors.append("邮箱格式不正确。")
        if not content:
            errors.append("评论内容不能为空。")
        if len(content) > 1000:
            errors.append("评论内容不能超过 1000 个字符。")
        return errors

    @staticmethod
    def create_pending(article, data, user=None):
        errors = CommentService.validate(data)
        if errors:
            return None, errors
        comment = Comment(
            article_id=article.id,
            user_id=user.id if user else None,
            nickname=normalize_text(data.get("nickname")),
            email=normalize_text(data.get("email")),
            content=normalize_text(data.get("content")),
            status=COMMENT_STATUS_PENDING,
        )
        db.session.add(comment)
        db.session.commit()
        return comment, []

    @staticmethod
    def approve(comment):
        comment.status = COMMENT_STATUS_APPROVED
        db.session.commit()

    @staticmethod
    def hide(comment):
        comment.status = COMMENT_STATUS_HIDDEN
        db.session.commit()

    @staticmethod
    def delete(comment):
        db.session.delete(comment)
        db.session.commit()
