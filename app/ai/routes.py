from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required

from app.ai.services import ai_service

ai_bp = Blueprint("ai", __name__, url_prefix="/admin/ai")


@ai_bp.route("/")
@login_required
def index():
    return render_template("admin/ai/index.html", message=ai_service.unavailable_message)


@ai_bp.route("/placeholder", methods=["POST"])
@login_required
def placeholder():
    flash(ai_service.unavailable_message, "info")
    return redirect(request.referrer or url_for("ai.index"))
