from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_migrate import Migrate

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()
mail = Mail()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # This is a basic configuration. In a real app, you'd use a config file.
    app.config['SECRET_KEY'] = 'your-super-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///real_estate.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'your-jwt-secret-key'

    # Email configuration
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USERNAME'] = 'your-email@gmail.com'  # Use environment variables for this
    app.config['MAIL_PASSWORD'] = 'your-password' # Use environment variables for this
    app.config['MAIL_DEFAULT_SENDER'] = 'your-email@gmail.com'

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)

    from . import models

    from .routes.auth import auth_bp
    from .routes.properties import properties_bp
    from .routes.listings import listings_bp
    from .routes.leads import leads_bp
    from .routes.deals import deals_bp
    from .routes.conversations import conversations_bp
    from .routes.messages import messages_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(properties_bp)
    app.register_blueprint(listings_bp)
    app.register_blueprint(leads_bp)
    app.register_blueprint(deals_bp)
    app.register_blueprint(conversations_bp)
    app.register_blueprint(messages_bp)

    from .errors import register_error_handlers
    register_error_handlers(app)

    return app