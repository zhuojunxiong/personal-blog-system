from functools import wraps

from flask import flash, redirect, url_for
from flask_login import current_user


def admin_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("请先登录管理员后台。", "warning")
            return redirect(url_for("auth.admin_login"))
        if not current_user.is_admin:
            flash("普通用户不能访问后台管理。", "danger")
            return redirect(url_for("public.index"))
        return view(*args, **kwargs)

    return wrapped
