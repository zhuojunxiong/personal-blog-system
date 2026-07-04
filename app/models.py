from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import db
from app.services import utcnow


ARTICLE_STATUS_DRAFT = "draft"
ARTICLE_STATUS_PUBLISHED = "published"
ARTICLE_STATUSES = (ARTICLE_STATUS_DRAFT, ARTICLE_STATUS_PUBLISHED)

COMMENT_STATUS_PENDING = "pending"
COMMENT_STATUS_APPROVED = "approved"
COMMENT_STATUS_HIDDEN = "hidden"
COMMENT_STATUSES = (
    COMMENT_STATUS_PENDING,
    COMMENT_STATUS_APPROVED,
    COMMENT_STATUS_HIDDEN,
)


class ArticleTag(db.Model):
    __tablename__ = "article_tags"

    article_id = db.Column(db.Integer, db.ForeignKey("articles.id"), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"), primary_key=True)
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    nickname = db.Column(db.String(64), nullable=False, default="知识创作者")
    role = db.Column(db.String(32), nullable=False, default="user")
    status = db.Column(db.String(32), nullable=False, default="active", index=True)
    bio = db.Column(db.String(500), default="")
    profile_markdown = db.Column(db.Text, default="")
    avatar = db.Column(db.String(255), default="")
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime,
        default=utcnow,
        onupdate=utcnow,
        nullable=False,
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method="pbkdf2:sha256")

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_active(self):
        return self.status == "active"

    @property
    def is_admin(self):
        return self.role == "admin"


class BlogColumn(db.Model):
    __tablename__ = "blog_columns"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(500), default="")
    status = db.Column(db.String(32), nullable=False, default="active")
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime,
        default=utcnow,
        onupdate=utcnow,
        nullable=False,
    )

    user = db.relationship("User", backref=db.backref("columns", lazy=True))
    # Note: When a column is deleted, articles have column_id set to NULL (nullable=True)
    articles = db.relationship("Article", back_populates="column")


class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False, index=True)
    description = db.Column(db.String(255), default="")
    sort_order = db.Column(db.Integer, default=0, nullable=False)
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime,
        default=utcnow,
        onupdate=utcnow,
        nullable=False,
    )

    # Note: Category deletion should check for existing articles first (nullable=False on Article.category_id)
    articles = db.relationship("Article", back_populates="category")


class Tag(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime,
        default=utcnow,
        onupdate=utcnow,
        nullable=False,
    )

    articles = db.relationship(
        "Article",
        secondary="article_tags",
        back_populates="tags",
    )


class Article(db.Model):
    __tablename__ = "articles"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(160), nullable=False, index=True)
    slug = db.Column(db.String(180), unique=True, nullable=False, index=True)
    summary = db.Column(db.String(500), default="")
    ai_search_summary = db.Column(db.Text, default="")
    ai_search_generated_at = db.Column(db.DateTime)
    content = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(32), nullable=False, default=ARTICLE_STATUS_DRAFT, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), index=True)
    column_id = db.Column(db.Integer, db.ForeignKey("blog_columns.id"), index=True)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False, index=True)
    author = db.Column(db.String(80), nullable=False, default="管理员")
    view_count = db.Column(db.Integer, nullable=False, default=0)
    like_count = db.Column(db.Integer, nullable=False, default=0)
    favorite_count = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime,
        default=utcnow,
        onupdate=utcnow,
        nullable=False,
    )
    published_at = db.Column(db.DateTime)

    user = db.relationship("User", backref=db.backref("articles", lazy=True))
    column = db.relationship("BlogColumn", back_populates="articles")
    category = db.relationship("Category", back_populates="articles")
    tags = db.relationship(
        "Tag",
        secondary="article_tags",
        back_populates="articles",
    )
    comments = db.relationship(
        "Comment",
        back_populates="article",
        cascade="all, delete-orphan",
    )
    ai_logs = db.relationship(
        "AiLog",
        back_populates="article",
        cascade="all, delete-orphan",
    )

    @property
    def approved_comment_count(self):
        from app.extensions import db
        from app.models import Comment, COMMENT_STATUS_APPROVED

        return db.session.query(db.func.count(Comment.id)).filter(
            Comment.article_id == self.id,
            Comment.status == COMMENT_STATUS_APPROVED,
        ).scalar() or 0


class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey("articles.id"), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), index=True)
    nickname = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(32), nullable=False, default=COMMENT_STATUS_PENDING)
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime,
        default=utcnow,
        onupdate=utcnow,
        nullable=False,
    )

    article = db.relationship("Article", back_populates="comments")
    user = db.relationship("User", backref=db.backref("comments", lazy=True))


class Like(db.Model):
    __tablename__ = "likes"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    article_id = db.Column(db.Integer, db.ForeignKey("articles.id"), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)

    user = db.relationship("User", backref=db.backref("likes", lazy=True))
    article = db.relationship("Article", backref=db.backref("likes", lazy=True, cascade="all, delete-orphan"))

    __table_args__ = (
        db.UniqueConstraint("user_id", "article_id", name="uq_user_article_like"),
    )


class Favorite(db.Model):
    __tablename__ = "favorites"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    article_id = db.Column(db.Integer, db.ForeignKey("articles.id"), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)

    user = db.relationship("User", backref=db.backref("favorites", lazy=True))
    article = db.relationship("Article", backref=db.backref("favorites", lazy=True, cascade="all, delete-orphan"))

    __table_args__ = (
        db.UniqueConstraint("user_id", "article_id", name="uq_user_article_favorite"),
    )


class AiLog(db.Model):
    __tablename__ = "ai_logs"

    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey("articles.id"), index=True)
    scene = db.Column(db.String(80), nullable=False)
    input_text = db.Column(db.Text, default="")
    ai_output = db.Column(db.Text, default="")
    adopted_result = db.Column(db.Text, default="")
    is_adopted = db.Column(db.Boolean, default=False, nullable=False)
    problem_found = db.Column(db.String(255), default="")
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)

    article = db.relationship("Article", back_populates="ai_logs")
