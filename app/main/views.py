#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random

from flask import flash, render_template, redirect, request, url_for
from flask_login import login_required, login_user
from sqlalchemy.sql import select
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, engine
from app.models import User, load_user
from app.tools import validate_email
from . import main



@main.route('/')
def index():
    return render_template('index.html', title='Kona - Возможности в твоих руках!', name='Абоб1')


@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        mail = User.query.filter_by(user_email=email).first()

        if mail:
            if check_password_hash(mail.user_password_hash, password):

                s = select(User.user_tag).where(User.user_email == email)
                tag = [row for row in engine.connect().execute(s)][0][0]

                login_user(mail, remember=True)

                return redirect(url_for('.user_profile', user_tag=tag))
            else:
                flash('Неверный пароль!', category='error')
        else:
            flash('Неверная почта!', category='error')
    return render_template('user_login.html', title='Kona | Вход')


@main.route('/registration', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        user_name = request.form['user_name']
        user_surname = request.form['user_surname']
        user_login = request.form['user_login']
        user_email = request.form['email']
        user_password = request.form['password']
        user_password_confirm = request.form['password_confirm']

        if len(user_name) > 0 \
                and len(user_surname) > 0 \
                and len(user_login) > 3 \
                and validate_email(user_email) \
                and (user_password == user_password_confirm):

            if User.query.filter_by(user_email=user_email).first():
                flash('Пользователь уже существует', 'error')
                return redirect(url_for('.login'))

            try:
                user_tag = random.randint(10_000_000, 99_999_999)
                while user_tag == User.query.filter_by(user_tag=user_tag).first():
                    user_tag = random.randint(10_000_000, 99_999_999)

                user = User(user_login=user_login, user_email=user_email,
                            user_password_hash=generate_password_hash(user_password), user_name=user_name,
                            user_surname=user_surname, user_tag=user_tag)
                db.session.add(user)
                db.session.flush()
                db.session.commit()

                return redirect(url_for('.login'))

            except:
                db.session.rollback()
                flash('Неизвестная ошибка. Повторите позже.', 'error')

        else:
            flash('Проверьте правильность введенных данных.', 'error')

    return render_template('user_registration.html', title='Kona | Регистрация')


@main.route('/user/<user_tag>', methods=['GET', 'POST'])
@login_required
def user_profile(user_tag):
    return render_template('user_profile.html', title=f'Kona | Личный кабинет {user_tag}')


@main.app_errorhandler(401)
def unauthorized(error):
    return redirect(url_for('.index'))


@main.app_errorhandler(404)
def page_not_found(error):
    return render_template('404.html', title="Kona | Страница не найдена"), 404
