# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify, request
from sqlalchemy import exc, or_

from project.api.models import User
from project import db, bcrypt


auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route('/auth/register', methods=['POST'])
def register_user():
	# get post data
	post_data = request.get_json()
	if not post_data:
		response_object = {
			'status': 'error',
			'message': 'Invalid payload.'
		}
		return jsonify(response_object), 400
	username = post_data.get('username')
	email = post_data.get('email')
	password = post_data.get('password')
	try:
		# check for existing user
		user = User.query.filter(
			or_(User.username == username, User.email == email)).first()
		if not user:
			new_user = User(
				username=username,
				email=email,
				password=password
			)
			db.session.add(new_user)
			db.session.commit()
			# generate auth token
			auth_token = new_user.encode_auth_token(new_user.id)
			response_object = {
				'status': 'success',
				'message': 'Successfully registered.',
				'auth_token': auth_token.decode()
			}
			return jsonify(response_object), 201
		else:
			response_object = {
				'status': 'error',
				'message': 'Sorry. That user already exists.'
			}
			return jsonify(response_object), 400
	# handle errors
	except (exc.IntegrityError, ValueError) as e:
		db.session.rollback()
		response_object = {
			'status': 'error',
			'message': 'Invalid payload.'
		}
		return jsonify(response_object), 400
