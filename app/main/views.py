#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from . import main
from app.models import User

from flask import Flask, flash, render_template, redirect, request, url_for
from flask_login import login_required, login_user, current_user, logout_user


@main.route('/')
def index():
    return render_template('index.html', title='Kona - Возможности в твоих руках!', name='Абоб1')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if len(request.form['email']) > 1:
            flash('TEST MESSAGE', 'error')

    return render_template('user_login.html', title='Kona | Вход')

@main.route('/registration', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        if len(request.form['user_name']) > 0 \
        and len(request.form['user_surname']) > 0 \
        and len(request.form['user_login']) > 4 \
        and len(request.form['email']) > 4 \
        and (request.form['password'] == request.form['password_confirm']):
            pass
        else:
            flash('Проверьте правильность введенных данных', 'error')
        
    return render_template('user_registration.html', title='Kona | Регистрация')

@main.app_errorhandler(404)
def page_not_found(error):
    return render_template('404.html', title="Kona | Страница не найдена"), 404