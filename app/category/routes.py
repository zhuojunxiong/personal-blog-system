from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required

from app.category.services import CategoryService

category_bp = Blueprint("category", __name__, url_prefix="/admin/categories")


@category_bp.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "POST":
        category, errors = CategoryService.create(request.form)
        if not errors:
            flash("分类创建成功。", "success")
            return redirect(url_for("category.index"))
        for error in errors:
            flash(error, "danger")
    return render_template("admin/categories/index.html", categories=CategoryService.all_ordered())


@category_bp.route("/<int:category_id>/edit", methods=["GET", "POST"])
@login_required
def edit(category_id):
    category = CategoryService.get_or_404(category_id)
    if request.method == "POST":
        errors = CategoryService.update(category, request.form)
        if not errors:
            flash("分类更新成功。", "success")
            return redirect(url_for("category.index"))
        for error in errors:
            flash(error, "danger")
    return render_template("admin/categories/form.html", category=category)


@category_bp.route("/<int:category_id>/delete", methods=["POST"])
@login_required
def delete(category_id):
    category = CategoryService.get_or_404(category_id)
    errors = CategoryService.delete(category)
    if errors:
        for error in errors:
            flash(error, "danger")
    else:
        flash("分类已删除。", "success")
    return redirect(url_for("category.index"))
