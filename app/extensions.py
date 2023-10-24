from flask_caching import Cache
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager



cache = Cache()
db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()
jwt = JWTManager()