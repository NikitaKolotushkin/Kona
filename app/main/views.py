#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
from datetime import datetime

from flask import flash, render_template, redirect, request, url_for, session, jsonify
from flask_login import login_required, login_user, current_user, logout_user
from sqlalchemy.orm import load_only
from sqlalchemy.sql import select, or_, and_

from app import engine, sio
from app.models import *
from app.tools import *
from . import main


@sio.event
def connect():
	print('connected ', request.sid)


@sio.event
def disconnect():
	print('disconnected ')


@sio.event
def message(data):
	print('message ', data)


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

				dict_relations = open_relations()
				dict_relations.update({user_tag: []})
				dump_relations(dict_relations)

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
	cities = [row[1] for row in engine.connect().execute(select(City))]
	universities = [row[1] for row in engine.connect().execute(select(University))]

	if request.method == 'POST':
		phone = request.form.get("phone")
		birthdate = datetime.strptime(request.form.get("birthdate"), '%Y-%m-%d')
		selected_city = request.form.get("city")
		selected_university = request.form.get("university")

		if len(phone) != 0:
			try:
				current_user.phone = phone
				current_user.birthdate = birthdate
				current_user.city_id = \
					[row for row in engine.connect().execute(select(City.id).where(City.name == selected_city))][0][0]
				current_user.university_id = [row for row in engine.connect().execute(
					select(University.id).where(University.name == selected_university))][0][0]
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
	table_keys = User.__table__.columns.keys()
	profile_owner = {}
	city_exists = user_data.city_id is not None
	university_exists = user_data.university_id is not None
	profile_owner['city_exists'] = city_exists
	profile_owner['university_exists'] = university_exists

	button_name = request.form.get('button_name')
	button_value = request.form.get('button_value')

	if button_name == 'accept_invite':
		if button_value == 'Принять заявку':
			try:
				pending_invite = [row for row in engine.connect().execute(
					select(Relations).where(and_(Relations.user_id == user_tag, Relations.friend_id == current_user.tag,
												 Relations.status == 'pending')))]
				operation_id = pending_invite[0][0]
				relation = Relations.query.get(operation_id)
				relation.status = 'accepted'
				db.session.commit()

				dict_relations = open_relations()
				if user_tag not in dict_relations[current_user.tag]:
					dict_relations[current_user.tag].append(user_tag)
				if current_user.tag not in dict_relations[user_tag]:
					dict_relations[user_tag].append(current_user.tag)
				dump_relations(dict_relations)
				data = {'message': 'Заявка принята'}
				return jsonify(data)
			except:
				db.session.rollback()
			return jsonify({'message': 'Неизвестная ошибка'})
		if button_value == 'Заявка принята':
			data = {'message': 'Заявка принята'}
			return jsonify(data)
	if button_name == 'add_friend':
		if button_value == 'Добавить в друзья':
			try:
				relations = Relations(user_id=current_user.tag, friend_id=user_tag)
				db.session.add(relations)
				db.session.flush()
				db.session.commit()
				data = {'message': 'Заявка отправлена'}
				return jsonify(data)
			except:
				db.session.rollback()
				return jsonify({'message': 'Неизвестная ошибка'})
		if button_value == 'Заявка отправлена':
			data = {'message': 'Заявка отправлена'}
			return jsonify(data)
	if button_name == 'write_message':
		return redirect(url_for('.messenger'))
	if button_name == 'make_graph':
		graph = open_relations()
		print(graph_maker(graph, current_user.tag, user_tag))

	friend_count = Relations.query.filter(or_(Relations.user_id == user_tag, Relations.friend_id == user_tag),
										  Relations.status == 'accepted').count()

	pending_invite = [row for row in engine.connect().execute(
		select(Relations).where(and_(Relations.user_id == user_tag, Relations.friend_id == current_user.tag,
									 Relations.status == 'pending')))]
	sent_invite = [row for row in engine.connect().execute(
		select(Relations).where(and_(Relations.user_id == current_user.tag, Relations.friend_id == user_tag,
									 Relations.status == 'pending')))]
	accepted_invite = [row for row in engine.connect().execute(
		select(Relations).where(
			or_((Relations.user_id == current_user.tag) & (Relations.friend_id == user_tag),
				(Relations.user_id == user_tag) &
				(Relations.friend_id == current_user.tag)),
			Relations.status == 'accepted'))]

	for key, value in zip(table_keys, user_data):
		profile_owner[key] = value
	if city_exists:
		profile_owner['city_id'] = City.query.get(user_data.city_id).name
	if university_exists:
		profile_owner['university_id'] = University.query.get(user_data.university_id).name

	return render_template('user_profile.html', title=f'Kona | {profile_owner["name"]} {profile_owner["surname"]}',
						   city_exists=city_exists, university_exists=university_exists,
						   pending_invite=pending_invite, accepted_invite=accepted_invite, sent_invite=sent_invite,
						   profile_owner=profile_owner, friend_count=friend_count)


@main.route('/friends', methods=['GET', 'POST'])
@login_required
def friends():
	query = [row for row in engine.connect().execute(
		select(Relations).where(or_(Relations.user_id == current_user.tag, Relations.friend_id == current_user.tag),
								Relations.status == 'accepted'))]

	friend_tags = [f[1] if f[1] != current_user.tag else f[2] for f in query]
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
	try:
		query = select(Messages).options(
			load_only(Messages.sender_id, Messages.receiver_id)).where(or_(Messages.sender_id == current_user.tag,
																		   Messages.receiver_id == current_user.tag))
	except:
		query = 0
	if query != 0:
		result = [row for row in engine.connect().execute(query)]

		unique_tags = {tag for sublist in result for tag in sublist[1:3] if tag != current_user.tag}
		dialogues = list(unique_tags)
		dialogue_list = [{} for _ in dialogues]

		for i in range(len(dialogues)):
			chat_data = [row for row in engine.connect().execute(select(User).where(User.tag == dialogues[i - 1]))][0]
			query = engine.connect().execute(select(Messages).order_by(Messages.id.desc()).where(
				or_(Messages.sender_id == dialogues[i - 1], Messages.receiver_id == dialogues[i - 1]))).first()
			last_message = query[3]
			time = query[4]
			dialogue_list[i - 1]['tag'] = chat_data[3]
			dialogue_list[i - 1]['name'] = chat_data[5]
			dialogue_list[i - 1]['surname'] = chat_data[6]
			dialogue_list[i - 1]['photo'] = chat_data[9]
			dialogue_list[i - 1]['last_message'] = last_message
			dialogue_list[i - 1]['time'] = time

	return render_template('messenger.html', title='Kona | Мессенджер', dialogue_list=dialogue_list)


@main.route('/message/<user_tag>', methods=['GET', 'POST'])
@login_required
def message(user_tag):
	return render_template('message.html', title='Kona | Сообщение', user_tag=user_tag)


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
