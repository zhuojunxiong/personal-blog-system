from flask import Flask, current_app
from sqlalchemy.exc import SQLAlchemyError

from app.extensions import csrf, db, login_manager
from config import Config


SQLITE_COMPAT_COLUMNS = {
    "users": {
        "profile_markdown": "TEXT DEFAULT ''",
    },
    "articles": {
        "ai_search_summary": "TEXT DEFAULT ''",
        "ai_search_generated_at": "DATETIME",
        "ai_review_status": "VARCHAR(32) DEFAULT 'pending' NOT NULL",
        "ai_review_reason": "TEXT DEFAULT ''",
        "ai_reviewed_at": "DATETIME",
        "ai_quality_score": "INTEGER",
        "ai_quality_report": "TEXT DEFAULT ''",
        "ai_quality_suggestions": "TEXT DEFAULT ''",
        "ai_quality_generated_at": "DATETIME",
    },
}


def create_app(config_class=Config):
    """Create and configure the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "请先登录后继续。"
    csrf.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User

        try:
            user_id = int(user_id)
        except (TypeError, ValueError):
            return None

        try:
            return User.query.get(user_id)
        except SQLAlchemyError:
            db.session.rollback()
            current_app.logger.warning("User lookup failed; checking SQLite schema.", exc_info=True)
            ensure_sqlite_schema(current_app._get_current_object())
            try:
                return User.query.get(user_id)
            except SQLAlchemyError:
                db.session.rollback()
                current_app.logger.exception("User lookup failed after SQLite schema recovery.")
                return None

    # ---- DEMO 模式：自动登录 ----
    demo_user = app.config.get("DEMO_AUTO_LOGIN")
    if demo_user:
        from flask import request
        from flask_login import login_user

        @app.before_request
        def demo_auto_login():
            from flask_login import current_user
            from app.models import User

            if current_user.is_authenticated:
                return
            user = User.query.filter_by(username=demo_user).first()
            if user:
                login_user(user)
                app.logger.info(f"[DEMO] 自动登录: {demo_user} (端口 {request.host.split(':')[-1] if ':' in request.host else '?'})")

    register_blueprints(app)
    register_error_handlers(app)
    register_template_helpers(app)
    ensure_sqlite_schema(app)

    return app


def ensure_sqlite_schema(app):
    """Auto-create tables on first run; add migration columns for existing databases."""
    if not app.config.get("SQLALCHEMY_DATABASE_URI", "").startswith("sqlite:///"):
        return
    from sqlalchemy import text

    # Ensure all models are imported before create_all
    from app import models  # noqa: F401

    with app.app_context():
        # Check if core tables exist; if not, create all tables from models
        with db.engine.connect() as conn:
            users_exists = conn.execute(
                text("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
            ).first()
        if not users_exists:
            db.create_all()
            app.logger.info("Database tables created automatically (first run).")

        # Add new columns for schema evolution (v0.5.1+ migrations)
        required_columns = {
            "users": {
                "profile_markdown": "TEXT DEFAULT ''",
            },
            "articles": {
                "ai_search_summary": "TEXT DEFAULT ''",
                "ai_search_generated_at": "DATETIME",
                "ai_review_status": "VARCHAR(32) DEFAULT 'pending' NOT NULL",
                "ai_review_reason": "TEXT DEFAULT ''",
                "ai_reviewed_at": "DATETIME",
                "ai_quality_score": "INTEGER",
                "ai_quality_report": "TEXT DEFAULT ''",
                "ai_quality_suggestions": "TEXT DEFAULT ''",
                "ai_quality_generated_at": "DATETIME",
            },
        }
        try:
            with db.engine.begin() as conn:
                for table, columns in required_columns.items():
                    table_exists = conn.execute(
                        text("SELECT name FROM sqlite_master WHERE type='table' AND name=:name"),
                        {"name": table},
                    ).first()
                    if not table_exists:
                        continue
                    existing = {
                        row[1]
                        for row in conn.execute(text(f"PRAGMA table_info({table})")).fetchall()
                    }
                    for column, definition in columns.items():
                        if column not in existing:
                            # SAFETY: table and column names come from hardcoded dict, not user input
                            conn.execute(text(f"ALTER TABLE {table} ADD COLUMN {column} {definition}"))
        except Exception:
            app.logger.exception("Failed to ensure SQLite compatibility columns.")


def register_blueprints(app):
    from app.admin.routes import admin_bp
    from app.ai.routes import ai_bp
    from app.article.routes import article_bp
    from app.auth.routes import auth_bp
    from app.category.routes import category_bp
    from app.column.routes import column_bp
    from app.comment.routes import comment_bp
    from app.dashboard.routes import dashboard_bp
    from app.public.routes import public_bp
    from app.tag.routes import tag_bp
    from app.user.routes import user_bp

    app.register_blueprint(public_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(article_bp)
    app.register_blueprint(column_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(tag_bp)
    app.register_blueprint(comment_bp)
    app.register_blueprint(ai_bp)
    app.register_blueprint(user_bp)


def register_error_handlers(app):
    from flask import render_template
    from werkzeug.exceptions import HTTPException

    @app.errorhandler(400)
    def bad_request(error):
        # CSRF validation failures are raised as 400 Bad Request
        desc = error.description if isinstance(error, HTTPException) else ""
        if desc and ("CSRF" in str(desc) or "csrf" in str(desc)):
            from flask import flash, redirect, request

            flash("表单验证已过期，请刷新页面后重试。", "warning")
            return redirect(request.referrer or "/")
        return render_template("errors/400.html"), 400

    @app.errorhandler(403)
    def forbidden(error):
        return render_template("errors/403.html"), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template("errors/500.html"), 500


def register_template_helpers(app):
    from flask import request, url_for
    from flask_wtf.csrf import generate_csrf
    from markupsafe import Markup, escape
    import re

    def render_markdown(text):
        text = text or ""
        lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
        html = []
        in_list = False
        in_code = False
        code_lines = []

        def close_list():
            nonlocal in_list
            if in_list:
                html.append("</ul>")
                in_list = False

        def inline(value):
            safe = escape(value)
            safe = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", str(safe))
            safe = re.sub(r"`([^`]+)`", r"<code>\1</code>", safe)
            safe = re.sub(
                r"\[([^\]]+)\]\((https?://[^)]+)\)",
                r'<a href="\2" target="_blank" rel="noopener noreferrer">\1</a>',
                safe,
            )
            return safe

        for raw_line in lines:
            line = raw_line.rstrip()
            if line.strip().startswith("```"):
                if in_code:
                    html.append(f"<pre><code>{escape(chr(10).join(code_lines))}</code></pre>")
                    code_lines = []
                    in_code = False
                else:
                    close_list()
                    in_code = True
                continue
            if in_code:
                code_lines.append(line)
                continue

            stripped = line.strip()
            if not stripped:
                close_list()
                continue
            if stripped.startswith("### "):
                close_list()
                html.append(f"<h3>{inline(stripped[4:])}</h3>")
            elif stripped.startswith("## "):
                close_list()
                html.append(f"<h2>{inline(stripped[3:])}</h2>")
            elif stripped.startswith("# "):
                close_list()
                html.append(f"<h1>{inline(stripped[2:])}</h1>")
            elif stripped.startswith(("- ", "* ")):
                if not in_list:
                    html.append("<ul>")
                    in_list = True
                html.append(f"<li>{inline(stripped[2:])}</li>")
            else:
                close_list()
                html.append(f"<p>{inline(stripped)}</p>")

        close_list()
        if in_code:
            html.append(f"<pre><code>{escape(chr(10).join(code_lines))}</code></pre>")
        return Markup("\n".join(html))

    app.add_template_filter(render_markdown, "markdown")

    @app.context_processor
    def inject_helpers():
        def page_url(page):
            args = dict(request.view_args or {})
            args.update(request.args.to_dict(flat=True))
            args["page"] = page
            return url_for(request.endpoint, **args)

        return {
            "page_url": page_url,
            "csrf_token_value": generate_csrf(),
        }
