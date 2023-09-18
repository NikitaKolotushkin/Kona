#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask
from config import DevelopmentConfig, TestingConfig, ProductionConfig


def create_app(config_class):

    app = Flask(__name__)
    app.config.from_object(config_class)

    register_blueprints(app)

    return app


def register_blueprints(app):
    from app.main import main

    app.register_blueprint(main)