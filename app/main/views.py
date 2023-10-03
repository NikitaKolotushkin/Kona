#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from . import main
from app.models import User

from flask import Flask, request, render_template, redirect, url_for
from flask_login import login_required, login_user, current_user, logout_user


@main.route('/')
def index():
    return render_template('index.html', title='Kona - Возможности в твоих руках!', name='Абоб1')

@main.route('/login')
def login():
    return render_template('user_login.html', title='Kona | Вход')

@main.route('/registration')
def registration():
    return render_template('user_registration.html', title='Kona | Регистрация')

@main.app_errorhandler(404)
def page_not_found(error):
    return render_template('404.html', title="Kona | Страница не найдена"), 404