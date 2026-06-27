from flask import Blueprint, flash, redirect, render_template, request, url_for
from app.admin.decorators import admin_required

from app.tag.services import TagService

tag_bp = Blueprint("tag", __name__, url_prefix="/admin/tags")


@tag_bp.route("/", methods=["GET", "POST"])
@admin_required
def index():
    if request.method == "POST":
        tag, errors = TagService.create(request.form)
        if not errors:
            flash("标签创建成功。", "success")
            return redirect(url_for("tag.index"))
        for error in errors:
            flash(error, "danger")
    return render_template("admin/tags/index.html", tags=TagService.all_ordered())


@tag_bp.route("/<int:tag_id>/edit", methods=["GET", "POST"])
@admin_required
def edit(tag_id):
    tag = TagService.get_or_404(tag_id)
    if request.method == "POST":
        errors = TagService.update(tag, request.form)
        if not errors:
            flash("标签更新成功。", "success")
            return redirect(url_for("tag.index"))
        for error in errors:
            flash(error, "danger")
    return render_template("admin/tags/form.html", tag=tag)


@tag_bp.route("/<int:tag_id>/delete", methods=["POST"])
@admin_required
def delete(tag_id):
    tag = TagService.get_or_404(tag_id)
    TagService.delete(tag)
    flash("标签已删除，文章关联关系已同步清理。", "success")
    return redirect(url_for("tag.index"))
