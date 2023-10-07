#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from . import main
from app.models import User
from app import db

from flask import Flask, flash, render_template, redirect, request, url_for
from flask_login import login_required, login_user, current_user, logout_user
from werkzeug.security import generate_password_hash


@main.route('/')
def index():
    return render_template('index.html', title='Kona - Возможности в твоих руках!', name='Абоб1')


@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        pass

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
        and len(user_email) > 4 \
        and (user_password == user_password_confirm):
            
            if User.query.filter_by(user_email=user_email).first():
                flash('Пользователь уже существует', 'error')
                return redirect(url_for('.login'))

            try:
                user = User(user_login=user_login, user_email=user_email, user_password_hash=generate_password_hash(user_password), user_name=user_name, user_surname=user_surname)
                db.session.add(user)
                db.session.flush()
                db.session.commit()

            except:
                db.session.rollback()
                flash('Неизвестная ошибка. Повторите позже.', 'error')
        
        else:
            flash('Проверьте правильность введенных данных.', 'error')
        
    return render_template('user_registration.html', title='Kona | Регистрация')


@main.app_errorhandler(401)
def unauthorized(error):
    return redirect(url_for('.index'))


@main.app_errorhandler(404)
def page_not_found(error):
    return render_template('404.html', title="Kona | Страница не найдена"), 404