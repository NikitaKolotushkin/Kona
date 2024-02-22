#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import codecs
import json
import random

from flask import flash, render_template, redirect, request, url_for, session
from flask_login import login_required, login_user, current_user, logout_user
from sqlalchemy.sql import select, or_
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, engine
from app.models import User, City, Relations
from app.tools import validate_email
from . import main


@main.route('/')
def index():
    if not current_user.is_authenticated:
        return render_template('index.html', title='Kona - Возможности в твоих руках!')
    else:
        return redirect(url_for('.events'))


@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password_hash, password):

                selected_user = select(User.tag).where(User.email == email)
                tag = [row for row in engine.connect().execute(selected_user)][0][0]

                login_user(user, remember=True)
                session.permanent = True
                session['email'] = user.email

                return redirect(url_for('.user_profile', user_tag=tag))
            else:
                flash('Неверный пароль!', category='error')
        else:
            flash('Неверная почта!', category='error')
    return render_template('user_login.html', title='Kona | Вход')


@main.route('/registration', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        user_name = request.form['user_name'].capitalize()
        user_surname = request.form['user_surname'].capitalize()
        user_login = request.form['user_login']
        user_email = request.form['email']
        user_password = request.form['password']
        user_password_confirm = request.form['password_confirm']

        if len(user_name) > 0 \
                and len(user_surname) > 0 \
                and len(user_login) > 3 \
                and validate_email(user_email) \
                and (user_password == user_password_confirm):

            if User.query.filter_by(email=user_email).first():
                flash('Пользователь уже существует', 'error')
                return redirect(url_for('.login'))

            try:
                user_tag = f'id{random.randint(10_000_000, 99_999_999)}'
                while user_tag == User.query.filter_by(tag=user_tag).first():
                    user_tag = f'id{random.randint(10_000_000, 99_999_999)}'

                user = User(login=user_login, email=user_email,
                            password_hash=generate_password_hash(user_password), name=user_name,
                            surname=user_surname, tag=user_tag)

                db.session.add(user)
                db.session.flush()
                db.session.commit()

                login_user(user, remember=True)
                session.permanent = True
                session['email'] = user.email

                return redirect(url_for('.questionnaire'))

            except:
                db.session.rollback()
                flash('Неизвестная ошибка. Повторите позже.', 'error')

        else:
            flash('Проверьте правильность введенных данных.', 'error')

    return render_template('user_registration.html', title='Kona | Регистрация')


@main.route('/questionnaire', methods=['GET', 'POST'])
@login_required
def questionnaire():
    with codecs.open('cities.json', 'r', 'utf_8_sig') as f:
        data = json.loads(f.read())

    cities = [row[1] for row in engine.connect().execute(select(City))]
    universities = sum([u for u in data.values() if len(u[0]) != 0], [])

    if request.method == 'POST':
        phone = request.form.get("phone")
        birthdate = request.form.get("birthdate")
        selected_city = request.form.get("city")
        selected_university = request.form.get("university")

        if len(phone) != 0:
            try:
                current_user.phone = phone
                current_user.birthdate = birthdate
                current_user.city_id = \
                    [row for row in engine.connect().execute(select(City.id).where(City.name == selected_city))][0][0]
                current_user.university = selected_university
                db.session.flush()
                db.session.commit()

                return redirect(url_for('.user_profile', user_tag=current_user.tag))

            except:
                db.session.rollback()
                flash('Неизвестная ошибка', 'error')

    return render_template('questionnaire.html', title='Kona | Анкета пользователя', cities=cities,
                           universities=universities)


@main.route('/user/<user_tag>', methods=['GET', 'POST'])
@login_required
def user_profile(user_tag):
    user_data = [row for row in engine.connect().execute(select(User).where(user_tag == User.tag))][0]
    table_keys = [key for key in engine.connect().execute(select(User)).keys()]
    university_exists, city_exists = False, False
    city = None

    query = [row for row in engine.connect().execute(
        select(Relations).where(or_(Relations.user_id == user_tag, Relations.friend_id == user_tag), Relations.status == 'accepted'))]
    friend_count = len(query)

    pending_invite = [row for row in engine.connect().execute(
        select(Relations).where(Relations.user_id == user_tag, Relations.friend_id == current_user.tag,
                                Relations.status == 'pending'))]
    sent_invite = [row for row in engine.connect().execute(
        select(Relations).where(Relations.user_id == current_user.tag, Relations.friend_id == user_tag,
                                Relations.status == 'pending'))]
    accepted_invite = [row for row in engine.connect().execute(
        select(Relations).where(Relations.user_id == current_user.tag, Relations.friend_id == user_tag,
                                Relations.status == 'accepted'))]
    reverse_accepted_invite = [row for row in engine.connect().execute(
        select(Relations).where(Relations.user_id == user_tag, Relations.friend_id == current_user.tag,
                                Relations.status == 'accepted'))]

    if request.method == 'POST':
        result = list(request.form.keys())[0]
        if pending_invite:
            if result == 'accept_invite':
                try:
                    operation_id = pending_invite[0][0]
                    relation = Relations.query.get(operation_id)
                    relation.status = 'accepted'
                    db.session.commit()
                except:
                    db.session.rollback()

        elif result == 'add_friend':
            try:
                relations = Relations(user_id=current_user.tag, friend_id=user_tag)
                db.session.add(relations)
                db.session.flush()
                db.session.commit()
            except:
                db.session.rollback()
                flash('Неизвестная ошибка', 'error')
        elif result == 'write_message':
            return redirect(url_for('.messenger'))

    profile_owner = {}

    for i in range(len(user_data)):
        profile_owner[table_keys[i]] = user_data[i]

    if profile_owner['university']:
        university_exists = True

    if profile_owner['city_id']:
        city = [x for x in engine.connect().execute(select(City).where(City.id == profile_owner['city_id']))][0][1]
        city_exists = city is not None if city else False

    return render_template('user_profile.html', title=f'Kona | {profile_owner["name"]} {profile_owner["surname"]}',
                           city=city, city_exists=city_exists, university_exists=university_exists,
                           pending_invite=pending_invite, accepted_invite=accepted_invite, sent_invite=sent_invite,
                           reverse_accepted_invite=reverse_accepted_invite,
                           profile_owner=profile_owner, friend_count=friend_count)


@main.route('/friends', methods=['GET', 'POST'])
@login_required
def friends():
    query = [row for row in engine.connect().execute(
        select(Relations).where(or_(Relations.user_id == current_user.tag, Relations.friend_id == current_user.tag),
                                Relations.status == 'accepted'))]

    friend_tags = [f[1] if f[1] != current_user.id else f[2] for f in query]
    friend_list = [{} for _ in range(len(query))]

    for f in range(len(friend_tags)):
        friend_data = [row for row in engine.connect().execute(select(User).where(User.tag == friend_tags[f - 1]))][0]
        friend_list[f - 1]['tag'] = friend_data[3]
        friend_list[f - 1]['name'] = friend_data[5]
        friend_list[f - 1]['surname'] = friend_data[6]
        friend_list[f - 1]['photo'] = friend_data[9]
        friend_list[f - 1]['university'] = friend_data[11]

    return render_template('friends.html', title='Kona | Друзья', friend_list=friend_list)


@main.route('/messenger', methods=['GET', 'POST'])
@login_required
def messenger():
    return render_template('messenger.html', title='Kona | Мессенджер')


@main.route('/message/<user_tag>', methods=['GET', 'POST'])
@login_required
def message(user_tag):
    return 1


@main.route('/events', methods=['GET', 'POST'])
@login_required
def events():
    return render_template('events.html', title='Kona | Мероприятия')


@main.route('/event/<event_id>', methods=['GET', 'POST'])
@login_required
def event_page(event_id):
    return render_template('event_page.html', title='Ивент')


@main.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('email', None)
    return redirect(url_for('.index'))


@main.app_errorhandler(401)
def unauthorized(error):
    return redirect(url_for('.index'))


@main.app_errorhandler(404)
def page_not_found(error):
    return render_template('404.html', title="Kona | Страница не найдена"), 404
