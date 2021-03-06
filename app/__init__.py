from flask import Flask
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap5
from config import config

moment = Moment()
db = SQLAlchemy()
bootstrap = Bootstrap5()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    moment.init_app(app)
    bootstrap.init_app(app)
    db.init_app(app)

    from app.usr import usr

    app.register_blueprint(usr)

    return app
