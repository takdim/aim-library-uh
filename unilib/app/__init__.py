from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os

from config import config

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
csrf = CSRFProtect()
limiter = Limiter(key_func=get_remote_address)

login_manager.login_view = 'auth.login'
login_manager.login_message = 'Silakan login untuk mengakses halaman ini.'
login_manager.login_message_category = 'warning'


def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Ensure upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)
    limiter.init_app(app)

    # Register blueprints
    from app.routes.public import public_bp
    from app.routes.auth import auth_bp
    from app.routes.staff import staff_bp
    from app.routes.admin import admin_bp

    app.register_blueprint(public_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(staff_bp, url_prefix='/dashboard')
    app.register_blueprint(admin_bp, url_prefix='/dashboard/admin')

    # Import models so Flask-Migrate sees them
    from app.models import user, news, profile, nav_link, service, statistic, activity_log  # noqa

    @login_manager.user_loader
    def load_user(user_id):
        from app.models.user import User
        return User.query.get(int(user_id))

    import re as _re
    @app.template_filter('html_preview')
    def html_preview(value):
        """Strip HTML tags, preserving bullet indicators for list items."""
        if not value:
            return ''
        text = _re.sub(r'<li[^>]*>', '• ', value, flags=_re.IGNORECASE)
        text = _re.sub(r'</(li|p|div|h[1-6])>', ' ', text, flags=_re.IGNORECASE)
        text = _re.sub(r'<br\s*/?>', ' ', text, flags=_re.IGNORECASE)
        text = _re.sub(r'<[^>]+>', '', text)
        text = _re.sub(r'\s+', ' ', text).strip()
        return text

    return app
