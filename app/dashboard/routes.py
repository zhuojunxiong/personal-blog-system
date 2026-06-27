from flask import Blueprint, render_template
from flask_login import login_required

from app.dashboard.services import DashboardService

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/admin")


@dashboard_bp.route("/dashboard")
@login_required
def index():
    return render_template("admin/dashboard.html", stats=DashboardService.stats())
