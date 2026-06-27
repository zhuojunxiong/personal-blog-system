from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user

from app.auth.services import AuthService
from app.models import User

auth_bp = Blueprint("auth", __name__)


def do_login(admin_only=False):
    if current_user.is_authenticated:
        if admin_only and not current_user.is_admin:
            flash("当前账号不是管理员，无法进入后台。", "danger")
            return redirect(url_for("public.index"))
        return redirect(url_for("dashboard.index") if current_user.is_admin else url_for("user.center"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password) and user.is_active:
            if admin_only and not user.is_admin:
                flash("普通用户不能登录后台。", "danger")
                return render_template("auth/login.html", admin_only=admin_only)
            login_user(user)
            flash("登录成功。", "success")
            next_url = request.args.get("next")
            if next_url:
                return redirect(next_url)
            return redirect(url_for("dashboard.index") if user.is_admin else url_for("user.center"))
        flash("用户名或密码错误，或账号已被禁用。", "danger")

    return render_template("auth/login.html", admin_only=admin_only)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    return do_login(admin_only=False)


@auth_bp.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    return do_login(admin_only=True)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("user.center"))
    if request.method == "POST":
        user, errors = AuthService.register(request.form)
        if not errors:
            login_user(user)
            flash("注册成功，欢迎创建自己的知识专栏。", "success")
            return redirect(url_for("user.center"))
        for error in errors:
            flash(error, "danger")
    return render_template("auth/register.html")


@auth_bp.route("/logout")
@auth_bp.route("/admin/logout")
def logout():
    logout_user()
    flash("已退出登录。", "info")
    return redirect(url_for("public.index"))
