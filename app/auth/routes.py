from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user

from app.models import User

auth_bp = Blueprint("auth", __name__, url_prefix="/admin")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password) and user.is_active:
            login_user(user)
            flash("登录成功，欢迎进入后台。", "success")
            next_url = request.args.get("next") or url_for("dashboard.index")
            return redirect(next_url)
        flash("用户名或密码错误。", "danger")

    return render_template("auth/login.html")


@auth_bp.route("/logout")
def logout():
    logout_user()
    flash("已退出登录。", "info")
    return redirect(url_for("auth.login"))
