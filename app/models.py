#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app import db, login_manager

from flask_login import LoginManager, UserMixin, login_required, login_user, current_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)


class User(db.Model, UserMixin):

    user_id = db.Column(db.Integer(), primary_key=True, nullable=False, unique=True)
    user_login = db.Column(db.String(64), nullable=False, unique=True)
    user_email = db.Column(db.String(64), nullable=False, unique=True)
    user_tag = db.Column(db.String(64), unique=True)
    user_password_hash = db.Column(db.String(256), nullable=False)
    user_name = db.Column(db.String(64), nullable=False)
    user_surname = db.Column(db.String(64), nullable=False)
    user_phone = db.Column(db.String(16), nullable=False)
    user_description = db.Column(db.Text(2048))
    user_photo = db.Column(db.LargeBinary(8000))
    user_city = db.Column(db.String(64))
    user_university = db.Column(db.String(255))

    def set_password(self, password):
        self.user_password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.user_password_hash, password)

    def __repr__(self):
        return f'<{self.id}:{self.username}>'