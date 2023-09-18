#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask

from app import create_app
from config import DevelopmentConfig, TestingConfig, ProductionConfig


app = create_app(config_class=DevelopmentConfig)

if __name__ == '__main__':
    app.run(host=app.config['HOST'], port=app.config['PORT'], debug=app.config['DEBUG'], use_reloader=app.config['RELOADER'])