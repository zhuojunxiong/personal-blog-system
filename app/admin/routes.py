from flask import Blueprint, redirect, url_for
from app.admin.decorators import admin_required

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/")
@admin_required
def index():
    return redirect(url_for("dashboard.index"))
