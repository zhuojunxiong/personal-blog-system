from flask import Flask

from app.extensions import csrf, db, login_manager
from config import Config


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

        return User.query.get(int(user_id))

    register_blueprints(app)
    register_error_handlers(app)
    register_template_helpers(app)

    return app


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
