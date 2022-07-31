from flask import Flask, render_template, session
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
import os
# from apps.config import config

db = SQLAlchemy()

csrf = CSRFProtect()

# create_app関数を作成する
def create_app():
    # Flaskインスタンス生成
    app = Flask(__name__)
    app.secret_key = "hogehoge"
    # app.config.from_object(config[config_key])
    # WEBSITE_HOSTNAME exists only in production environment
    if not 'WEBSITE_HOSTNAME' in os.environ:
          # local development, where we'll use environment variables
        print("Loading config.development and environment variables from .env file.")
        app.config.from_object('azureproject.development')
    else:
        # production
        print("Loading config.production.")
        app.config.from_object('azureproject.production')
    
    print(app.config.get('DATABASE_URI'))
    app.config.update(
        SQLALCHEMY_DATABASE_URI=app.config.get('DATABASE_URI'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_ECHO=True,
        WTF_CSRF_SECRET_KEY = "AuwzyszU5sugKN7KZs6f"
    )
    csrf.init_app(app)

    db.init_app(app)
    Migrate(app, db)

    from crud.models import User

    # crudパッケージからviewsをimportする
    # from apps.crud import views as crud_views
    from crud import views as crud_views

    # register_blueprintを使いviewsのcrudをアプリへ登録する
    app.register_blueprint(crud_views.crud, url_prefix="/crud")

    return app