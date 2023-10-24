import os
from datetime import timedelta

from dotenv import load_dotenv


load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))


class ConfigBase:
    API_KEY_RAWG = os.getenv('API_KEY_RAWG')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=int(os.getenv('HOURS_TO_JWT_ACCESS_TOKEN_EXPIRES')))
    BASE_URL_RAWG = os.getenv('BASE_URL_RAWG')
    FLASK_DEBUG = False
    FLASK_APP = os.getenv('FLASK_APP')
    PROPAGATE_EXCEPTIONS = True


class Config(ConfigBase):
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')
    FLASK_DEBUG = os.getenv('DEBUG')
    CACHE_TYPE= os.getenv('CACHE_TYPE')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')


class ConfigTest(ConfigBase):
    FLASK_DEBUG = True
    SECRET_KEY = "secret_key_to_test"
    SQLALCHEMY_DATABASE_URI =  'sqlite:///' + os.path.join(basedir, 'test.sqlite')
    CACHE_TYPE = 'flask_caching.backends.SimpleCache'
    JWT_SECRET_KEY = 'secret_key_to_jwt'