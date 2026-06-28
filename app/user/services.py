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

    @staticmethod
    def change_password(user, data):
        old_password = data.get("old_password") or ""
        new_password = data.get("new_password") or ""
        confirm_password = data.get("confirm_password") or ""
        errors = []
        if not old_password:
            errors.append("请输入当前密码。")
        if not new_password:
            errors.append("请输入新密码。")
        elif len(new_password) < 6:
            errors.append("新密码至少需要 6 位。")
        if new_password != confirm_password:
            errors.append("两次输入的新密码不一致。")
        if old_password and not user.check_password(old_password):
            errors.append("当前密码不正确。")
        if errors:
            return errors
        user.set_password(new_password)
        db.session.commit()
        return []
