from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

# login mechanism
from flask_login import LoginManager

db = SQLAlchemy()

BASE_DIR = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))
SUB_DIR = "database/python-web-app-1"
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{path.join(BASE_DIR, SUB_DIR, DB_NAME)}"
    app.config["SECRET_KEY"] = "secret key"

    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    # create database if the database did not exist
    try:  
        if not path.exists(app.config['SQLALCHEMY_DATABASE_URI']):
            with app.app_context():
                db.create_all()
                print("Created database.")
    except:
        print("Failed to initialize database.")

    from .models import User

    # # login mechanism
    login_manager = LoginManager()
    login_manager.login_view = "auth.login" # where to redirect if not logged in
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app