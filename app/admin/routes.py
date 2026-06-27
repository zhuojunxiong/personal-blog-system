from flask import Blueprint, redirect, url_for
from flask_login import login_required

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/")
@login_required
def index():
    return redirect(url_for("dashboard.index"))
