from flask import Flask

from app.extensions import db, login_manager
from config import Config


def create_app(config_class=Config):
    """Create and configure the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "请先登录管理员后台。"

    @login_manager.user_loader
    def load_user(user_id):
        return None

    register_blueprints(app)

    return app


def register_blueprints(app):
    from app.public.routes import public_bp

    app.register_blueprint(public_bp)
