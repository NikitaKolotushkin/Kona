#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app import db, login_manager

from flask_login import LoginManager, UserMixin, login_required, login_user, current_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash


class User(db.Model, UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer(), primary_key=True, nullable=False, unique=True)
    login = db.Column(db.String(64), nullable=False, unique=True)
    email = db.Column(db.String(64), nullable=False, unique=True)
    tag = db.Column(db.String(64), nullable=False, unique=True)
    password_hash = db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(64), nullable=False)
    surname = db.Column(db.String(64), nullable=False)
    phone = db.Column(db.String(16))
    description = db.Column(db.Text(2048))
    photo = db.Column(db.LargeBinary(8000))
    city_id = db.Column(db.String(64))
    university = db.Column(db.String(255))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<{self.id}:{self.name}>'
    

class University(db.Model):
    
    __tablename__ = 'universities'

    id = db.Column(db.Integer(), primary_key=True, nullable=False, unique=True)
    name = db.Column(db.String(255), nullable=True, unique=True)
    city = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return f'<{self.id}:{self.name}>'
    

class City(db.Model):

    __tablename__ = 'cities'

    id = db.Column(db.Integer(), primary_key=True, nullable=False, unique=True)
    name = db.Column(db.String(128), nullable=False, unique=True)

    def __repr__(self):
        return f'<{self.id}:{self.name}>'


class Interest(db.Model):

    __tablename__ = 'interests'

    id = db.Column(db.Integer(), primary_key=True, nullable=False, unique=True)
    name = db.Column(db.String(255), nullable=False, unique=True)

    def __repr__(self):
        return f'<{self.id}:{self.name}>'


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)
