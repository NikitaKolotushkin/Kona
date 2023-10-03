#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from config import DevelopmentConfig, TestingConfig, ProductionConfig


db = SQLAlchemy()
login_manager = LoginManager()


def create_app(config_class):

    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)


    from .main import main as main_blueprint


    app.register_blueprint(main_blueprint)
    return app


def register_blueprints(app):
    from app.main import main

    app.register_blueprint(main)