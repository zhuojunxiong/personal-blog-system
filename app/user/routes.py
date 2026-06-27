from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.admin.decorators import admin_required
from app.article.services import ArticleService
from app.category.services import CategoryService
from app.column.services import ColumnService
from app.services import parse_int_list
from app.tag.services import TagService
from app.user.services import UserService

user_bp = Blueprint("user", __name__)


@user_bp.route("/users/<int:user_id>")
def profile(user_id):
    user = UserService.get_or_404(user_id)
    return render_template(
        "public/user_profile.html",
        profile_user=user,
        columns=ColumnService.by_user(user.id),
        articles=ArticleService.published_by_user(user.id),
    )


@user_bp.route("/me")
@login_required
def center():
    return render_template(
        "user/center.html",
        columns=ColumnService.by_user(current_user.id),
        articles=ArticleService.list_by_user(current_user.id),
        interactions=UserService.interaction_summary(current_user),
    )


@user_bp.route("/me/profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    if request.method == "POST":
        errors = UserService.update_profile(current_user, request.form)
        if not errors:
            flash("个人资料已更新。", "success")
            return redirect(url_for("user.center"))
        for error in errors:
            flash(error, "danger")
    return render_template("user/profile_form.html")


@user_bp.route("/write", methods=["GET", "POST"])
@login_required
def write_article():
    categories = CategoryService.all_ordered()
    tags = TagService.all_ordered()
    columns = ColumnService.by_user(current_user.id)
    if request.method == "POST":
        article, errors = ArticleService.create(
            request.form,
            parse_int_list(request.form.getlist("tag_ids")),
            user=current_user,
        )
        if not errors:
            flash("文章保存成功。", "success")
            return redirect(url_for("user.center"))
        for error in errors:
            flash(error, "danger")
    return render_template(
        "user/article_form.html",
        article=None,
        categories=categories,
        tags=tags,
        columns=columns,
    )


@user_bp.route("/my/articles/<int:article_id>/edit", methods=["GET", "POST"])
@login_required
def edit_article(article_id):
    article = ArticleService.get_or_404(article_id)
    if article.user_id != current_user.id and not current_user.is_admin:
        abort(403)
    categories = CategoryService.all_ordered()
    tags = TagService.all_ordered()
    columns = ColumnService.by_user(current_user.id)
    if request.method == "POST":
        errors = ArticleService.update(article, request.form, parse_int_list(request.form.getlist("tag_ids")))
        if not errors:
            flash("文章更新成功。", "success")
            return redirect(url_for("user.center"))
        for error in errors:
            flash(error, "danger")
    return render_template(
        "user/article_form.html",
        article=article,
        categories=categories,
        tags=tags,
        columns=columns,
    )


@user_bp.route("/my/articles/<int:article_id>/delete", methods=["POST"])
@login_required
def delete_article(article_id):
    article = ArticleService.get_or_404(article_id)
    if article.user_id != current_user.id and not current_user.is_admin:
        abort(403)
    ArticleService.delete(article)
    flash("文章已删除。", "success")
    return redirect(url_for("user.center"))


@user_bp.route("/admin/users")
@admin_required
def admin_users():
    return render_template("admin/users/index.html", users=UserService.all_users())


@user_bp.route("/admin/users/<int:user_id>/toggle", methods=["POST"])
@admin_required
def admin_toggle_user(user_id):
    user = UserService.get_or_404(user_id)
    if user.is_admin:
        flash("不能禁用管理员账号。", "danger")
    else:
        UserService.set_status(user, "disabled" if user.status == "active" else "active")
        flash("用户状态已更新。", "success")
    return redirect(url_for("user.admin_users"))
