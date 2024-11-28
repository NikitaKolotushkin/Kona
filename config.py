import os

from datetime import timedelta

app_dir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    SECRET_KEY = 'SECRET_KEY'
    FLASK_JWT_SECRET_KEY = 'fuckinginsane'
    JWT_TOKEN_LOCATION = ['cookies']
    JWT_COOKIE_CSRF_PROTECT = True
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    JWT_COOKIE_SAMESITE = "Strict"
    DEBUG = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = ''
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TEMPLATES_AUTO_RELOAD = True
    COOKIE_SECURE = 'Secure'
    COOKIE_DURATION = timedelta(days=31)
    SESSION_PERMANENT = True
    PERMANENT_SESSION_LIFETIME = timedelta(days=31)
    REMEMBER_COOKIE_DURATION = timedelta(days=31)
    UPLOAD_FOLDER = os.path.join(app_dir, 'uploads')
    JSON_AS_ASCII = True
    HOST = os.environ.get('APP_HOST', '0.0.0.0')
    PORT = int(os.environ.get('APP_PORT', 5000))
    RELOADER = False


class DevelopmentConfig(BaseConfig):
    DEVELOPMENT = True
    DEBUG = True
    RELOADER = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEVELOPMENT_DATABASE_URI') or 'sqlite:///' + os.path.join(app_dir,
                                                                                                        'app/databases/dev.db')


class TestingConfig(BaseConfig):
    DEBUG = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TESTING_DATABASE_URI') or 'sqlite:///' + os.path.join(app_dir,
                                                                                                    'app/databases/test.db')


class ProductionConfig(BaseConfig):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('PRODUCTION_DATABASE_URI') or 'sqlite:///' + os.path.join(app_dir,
                                                                                                       'app/databases/site.db')


current_config = DevelopmentConfig
