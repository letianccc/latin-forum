import os

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_pagedown import PageDown
from flask_moment import Moment

from app.auth import auth as auth_blueprint
from app.main.blueprint import main

from config import config

basedir = os.path.abspath(os.path.dirname(__file__))
bootstrap = Bootstrap()
manager = Manager()
db = SQLAlchemy()
pagedown = PageDown()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
moment = Moment()




def create_app(config_name=None):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)



    # app.config['SECRET_KEY'] = 'hard to guess string'
    # app.config['SQLALCHEMY_DATABASE_URI'] =\
    # 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # app.config['FLASKY_POSTS_PER_PAGE'] = 20
    # app.config['FLASKY_COMMENTS_PER_PAGE'] = 10

    app.register_blueprint(main)
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    pagedown.init_app(app)
    moment.init_app(app)

    return app
