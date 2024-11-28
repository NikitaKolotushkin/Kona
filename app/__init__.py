#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

from config import current_config


db = SQLAlchemy()
engine = create_engine(current_config.SQLALCHEMY_DATABASE_URI)
login_manager = LoginManager()
migrate = Migrate()
sio = SocketIO()
jwt = JWTManager()


def create_app(config_class):
	app = Flask(__name__)
	app.config.from_object(config_class)

	db.init_app(app)

	with app.app_context():
		if db.engine.url.drivername == 'sqlite':
			migrate.init_app(app, db, render_as_batch=True)
		else:
			migrate.init_app(app, db)

	login_manager.init_app(app)
	login_manager.login_view = 'main.login'
	sio.init_app(app)
	jwt.init_app(app)

	from .main import main as main_blueprint

	app.register_blueprint(main_blueprint)
	return app, sio


def register_blueprints(app):
	from app.main import main

	app.register_blueprint(main)
