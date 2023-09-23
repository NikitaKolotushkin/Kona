#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from . import main

from flask import Flask, request, render_template, redirect, url_for


@main.route('/')
@main.route('/index')
def index():
    return render_template('index.html', title='Kona - Возможности в твоих руках!', name='Абоб')

@main.route('/login')
def login():
    return render_template('user_login.html', title='Kona | Вход')

@main.route('/registration')
def registration():
    return render_template('user_registration.html', title='Kona | Регистрация')