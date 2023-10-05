import os
import random
import string


app_dir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY') or "".join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(25))
    DEBUG = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = ''
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TEMPLATES_AUTO_RELOAD = True
    UPLOAD_FOLDER: str = os.path.join(app_dir, 'uploads')
    JSON_AS_ASCII: bool = True
    HOST: str = os.environ.get('APP_HOST', '0.0.0.0')
    PORT: int = int(os.environ.get('APP_PORT', 8080))
    RELOADER = False


class DevelopmentConfig(BaseConfig):
    DEVELOPMENT = True
    DEBUG = True
    RELOADER = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEVELOPMENT_DATABASE_URI') or 'sqlite:///' + os.path.join(app_dir, 'app/databases/dev.db')


class TestingConfig(BaseConfig):
    DEBUG = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TESTING_DATABASE_URI') or 'sqlite:///' + os.path.join(app_dir, 'app/databases/test.db')


class ProductionConfig(BaseConfig):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('PRODUCTION_DATABASE_URI') or 'sqlite:///' + os.path.join(app_dir, 'app/databases/site.db')


current_config = DevelopmentConfig