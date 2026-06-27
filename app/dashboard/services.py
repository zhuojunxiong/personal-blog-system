from app.models import (
    ARTICLE_STATUS_DRAFT,
    ARTICLE_STATUS_PUBLISHED,
    COMMENT_STATUS_PENDING,
    Article,
    BlogColumn,
    Category,
    Comment,
    Tag,
    User,
)


class DashboardService:
    @staticmethod
    def stats():
        return {
            "article_count": Article.query.count(),
            "published_count": Article.query.filter_by(status=ARTICLE_STATUS_PUBLISHED).count(),
            "draft_count": Article.query.filter_by(status=ARTICLE_STATUS_DRAFT).count(),
            "category_count": Category.query.count(),
            "tag_count": Tag.query.count(),
            "user_count": User.query.count(),
            "column_count": BlogColumn.query.count(),
            "comment_count": Comment.query.count(),
            "pending_comment_count": Comment.query.filter_by(status=COMMENT_STATUS_PENDING).count(),
            "recent_articles": Article.query.order_by(Article.created_at.desc()).limit(5).all(),
            "latest_comments": Comment.query.order_by(Comment.created_at.desc()).limit(5).all(),
        }
