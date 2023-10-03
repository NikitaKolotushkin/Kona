#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask_script import Command

from config import DevelopmentConfig, TestingConfig, ProductionConfig


class Runner(Command):
    'Запуск приложения с заранее заданными параметрами'

    def __init__(self, app):
        self.app = app

    def run(self):
        return self.app.run(host=self.app.config['HOST'], port=self.app.config['PORT'], debug=self.app.config['DEBUG'], use_reloader=self.app.config['RELOADER'])