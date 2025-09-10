from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

# login mechanism
from flask_login import LoginManager

db = SQLAlchemy()

DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)

    basedir = path.abspath("instance/")

    app.config["SECRET_KEY"] = "secret key"

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + path.join(basedir, DB_NAME)

    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from .models import User, Note

    if not path.exists("instance/" + DB_NAME):
        with app.app_context():
            db.create_all()
            print("Created database.")

    # # login mechanism
    login_manager = LoginManager()
    login_manager.login_view = "auth.login" # where to redirect if not logged in
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app