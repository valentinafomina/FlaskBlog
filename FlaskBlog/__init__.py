from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail

from FlaskBlog.config import Config

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
mail = Mail()


def create_app():
    print(__name__)
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)

    from FlaskBlog.main.routes import main
    from FlaskBlog.auth.routes import users
    from FlaskBlog.postapp.routes import posts
    from FlaskBlog.errors.handlers import errors
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(errors)

    return app