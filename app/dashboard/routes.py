from flask import Blueprint, render_template
from app.admin.decorators import admin_required

from app.dashboard.services import DashboardService

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/admin")


@dashboard_bp.route("/dashboard")
@admin_required
def index():
    return render_template("admin/dashboard.html", stats=DashboardService.stats())
