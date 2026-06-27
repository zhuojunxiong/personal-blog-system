from app.extensions import db
from app.models import User
from app.services import normalize_text


class AuthService:
    @staticmethod
    def validate_register(data):
        errors = []
        username = normalize_text(data.get("username"))
        email = normalize_text(data.get("email"))
        password = data.get("password") or ""
        if not username:
            errors.append("用户名不能为空。")
        if len(username) > 64:
            errors.append("用户名不能超过 64 个字符。")
        if not email or "@" not in email:
            errors.append("邮箱格式不正确。")
        if len(password) < 6:
            errors.append("密码至少需要 6 位。")
        if username and User.query.filter_by(username=username).first():
            errors.append("用户名已存在。")
        if email and User.query.filter_by(email=email).first():
            errors.append("邮箱已被注册。")
        return errors

    @staticmethod
    def register(data):
        errors = AuthService.validate_register(data)
        if errors:
            return None, errors
        user = User(
            username=normalize_text(data.get("username")),
            email=normalize_text(data.get("email")),
            nickname=normalize_text(data.get("nickname")) or normalize_text(data.get("username")),
            role="user",
            status="active",
            bio=normalize_text(data.get("bio")),
        )
        user.set_password(data.get("password"))
        db.session.add(user)
        db.session.commit()
        return user, []
