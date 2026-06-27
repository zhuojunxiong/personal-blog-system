from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import db


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
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    nickname = db.Column(db.String(64), nullable=False, default="管理员")
    role = db.Column(db.String(32), nullable=False, default="admin")
    status = db.Column(db.String(32), nullable=False, default="active")
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_active(self):
        return self.status == "active"


class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False, index=True)
    description = db.Column(db.String(255), default="")
    sort_order = db.Column(db.Integer, default=0, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    articles = db.relationship("Article", back_populates="category")


class Tag(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
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
    content = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(32), nullable=False, default=ARTICLE_STATUS_DRAFT)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)
    author = db.Column(db.String(80), nullable=False, default="管理员")
    view_count = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )
    published_at = db.Column(db.DateTime)

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
        return len([c for c in self.comments if c.status == COMMENT_STATUS_APPROVED])


class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey("articles.id"), nullable=False)
    nickname = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(32), nullable=False, default=COMMENT_STATUS_PENDING)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    article = db.relationship("Article", back_populates="comments")


class AiLog(db.Model):
    __tablename__ = "ai_logs"

    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey("articles.id"))
    scene = db.Column(db.String(80), nullable=False)
    input_text = db.Column(db.Text, default="")
    ai_output = db.Column(db.Text, default="")
    adopted_result = db.Column(db.Text, default="")
    is_adopted = db.Column(db.Boolean, default=False, nullable=False)
    problem_found = db.Column(db.String(255), default="")
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    article = db.relationship("Article", back_populates="ai_logs")
