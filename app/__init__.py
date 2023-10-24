from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import Config
from .extensions import cache, db, migrate, ma, jwt


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    cache.init_app(app)
    jwt.init_app(app)

    from commands import init_app
    init_app(app)

    from app.api import api
    api.init_app(app)        

    from app.api.errors import configure_error_handlers 
    configure_error_handlers(app)

    return app


