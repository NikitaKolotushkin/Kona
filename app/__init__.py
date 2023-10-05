#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import DevelopmentConfig, TestingConfig, ProductionConfig


db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()


def create_app(config_class):

    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'
    migrate.init_app(app, db)


    from .main import main as main_blueprint


    app.register_blueprint(main_blueprint)
    return app


def register_blueprints(app):
    from app.main import main

    app.register_blueprint(main)