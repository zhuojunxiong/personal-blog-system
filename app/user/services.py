from app.extensions import db
from app.models import Comment, Favorite, Like, User
from app.services import normalize_text


class UserService:
    @staticmethod
    def get_or_404(user_id):
        return User.query.get_or_404(user_id)

    @staticmethod
    def all_users():
        return User.query.order_by(User.created_at.desc()).all()

    @staticmethod
    def update_profile(user, data):
        nickname = normalize_text(data.get("nickname"))
        email = normalize_text(data.get("email"))
        bio = normalize_text(data.get("bio"))
        errors = []
        if not nickname:
            errors.append("昵称不能为空。")
        if not email or "@" not in email:
            errors.append("邮箱格式不正确。")
        existing = User.query.filter(User.email == email, User.id != user.id).first()
        if existing:
            errors.append("邮箱已被其他用户使用。")
        if errors:
            return errors
        user.nickname = nickname
        user.email = email
        user.bio = bio
        db.session.commit()
        return []

    @staticmethod
    def set_status(user, status):
        user.status = status
        db.session.commit()

    @staticmethod
    def interaction_summary(user):
        return {
            "comments": Comment.query.filter_by(user_id=user.id).order_by(Comment.created_at.desc()).all(),
            "likes": Like.query.filter_by(user_id=user.id).order_by(Like.created_at.desc()).all(),
            "favorites": Favorite.query.filter_by(user_id=user.id).order_by(Favorite.created_at.desc()).all(),
        }
