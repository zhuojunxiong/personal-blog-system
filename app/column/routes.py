from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.admin.decorators import admin_required
from app.article.services import ArticleService
from app.column.services import ColumnService

column_bp = Blueprint("column", __name__)


@column_bp.route("/columns")
def index():
    return render_template("public/columns.html", columns=ColumnService.all_active())


@column_bp.route("/columns/<int:column_id>")
def detail(column_id):
    column = ColumnService.get_or_404(column_id)
    if column.status != "active" and not (current_user.is_authenticated and current_user.id == column.user_id):
        abort(404)
    return render_template(
        "public/column_detail.html",
        column=column,
        articles=ArticleService.published_by_column(column.id),
    )


@column_bp.route("/my/columns", methods=["GET", "POST"])
@login_required
def my_columns():
    if request.method == "POST":
        column, errors = ColumnService.create(request.form, current_user)
        if not errors:
            flash("专栏创建成功。", "success")
            return redirect(url_for("column.my_columns"))
        for error in errors:
            flash(error, "danger")
    return render_template("user/columns.html", columns=ColumnService.by_user(current_user.id))


@column_bp.route("/my/columns/<int:column_id>/edit", methods=["GET", "POST"])
@login_required
def edit(column_id):
    column = ColumnService.get_or_404(column_id)
    if column.user_id != current_user.id and not current_user.is_admin:
        abort(403)
    if request.method == "POST":
        errors = ColumnService.update(column, request.form)
        if not errors:
            flash("专栏更新成功。", "success")
            return redirect(url_for("column.my_columns"))
        for error in errors:
            flash(error, "danger")
    return render_template("user/column_form.html", column=column)


@column_bp.route("/my/columns/<int:column_id>/delete", methods=["POST"])
@login_required
def delete(column_id):
    column = ColumnService.get_or_404(column_id)
    if column.user_id != current_user.id and not current_user.is_admin:
        abort(403)
    errors = ColumnService.delete(column)
    if errors:
        for error in errors:
            flash(error, "danger")
    else:
        flash("专栏已删除。", "success")
    return redirect(url_for("column.my_columns"))


@column_bp.route("/admin/columns")
@admin_required
def admin_index():
    return render_template("admin/columns/index.html", columns=ColumnService.all_active())


@column_bp.route("/admin/columns/<int:column_id>/toggle", methods=["POST"])
@admin_required
def admin_toggle(column_id):
    column = ColumnService.get_or_404(column_id)
    column.status = "disabled" if column.status == "active" else "active"
    from app.extensions import db

    db.session.commit()
    flash("专栏状态已更新。", "success")
    return redirect(url_for("column.admin_index"))
