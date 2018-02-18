# -*- coding: utf-8 -*-

import json
import time

from project import db
from project.api.models import User
from project.tests.base import BaseTestCase
from project.tests.utils import add_user


class TestAuthBlueprint(BaseTestCase):

	def test_user_registration(self):
		with self.client:
			response = self.client.post(
				'/auth/register',
				data=json.dumps(dict(
					username='testuser',
					email='user@test.com',
					password='123456'
				)),
				content_type='application/json'
			)
			data = json.loads(response.data.decode())
			self.assertTrue(data['status'] == 'success')
			self.assertTrue(data['message'] == 'Successfully registered.')
			self.assertTrue(data['auth_token'])
			self.assertTrue(response.content_type == 'application/json')
			self.assertEqual(response.status_code, 201)

	def test_user_registration_duplicate_email(self):
		add_user('testuser2', 'user@test.com', '123456')
		with self.client:
			response = self.client.post(
				'/auth/register',
				data=json.dumps(dict(
					username='testuser',
					email='user@test.com',
					password='123456'
				)),
				content_type='application/json'
			)
			data = json.loads(response.data.decode())
			self.assertEqual(response.status_code, 400)
			self.assertIn('Sorry. That user already exists.', data['message'])
			self.assertIn('error', data['status'])

	def test_user_registration_invalid_json(self):
		with self.client:
			response = self.client.post(
				'/auth/register',
				data=json.dumps(dict()),
				content_type='application/json'
			)
			data = json.loads(response.data.decode())
			self.assertEqual(response.status_code, 400)
			self.assertIn('Invalid payload.', data['message'])
			self.assertIn('error', data['status'])

	def test_user_registration_invalid_json_keys_no_username(self):
		with self.client:
			response = self.client.post(
				'/auth/register',
				data=json.dumps(dict(email='user@test.com', password='1234')),
				content_type='application/json'
			)
			data = json.loads(response.data.decode())
			self.assertEqual(response.status_code, 400)
			self.assertIn('Invalid payload.', data['message'])
			self.assertIn('error', data['status'])

	def test_user_registration_invalid_json_keys_no_email(self):
		with self.client:
			response = self.client.post(
				'/auth/register',
				data=json.dumps(dict(username='testuser', password='1234')),
				content_type='application/json'
			)
			data = json.loads(response.data.decode())
			self.assertEqual(response.status_code, 400)
			self.assertIn('Invalid payload.', data['message'])
			self.assertIn('error', data['status'])

	def test_registered_user_login(self):
		with self.client:
			user = add_user('user', 'user@test.com', '1234')
			response = self.client.post(
				'/auth/login',
				data=json.dumps(dict(
						email='user@test.com',
						password='1234'
					)),
					content_type='application/json'
			)
			data = json.loads(response.data.decode())
			self.assertTrue(data['status'] == 'success')
			self.assertTrue(data['message'] == 'Successfully loged in.')
			self.assertTrue(data['auth_token'])
			self.assertTrue(response.content_type == 'application/json')
			self.assertEqual(response.status_code, 200)

	def test_not_registered_user_login(self):
		with self.client:
			response = self.client.post(
				'/auth/login',
				data=json.dumps(dict(
						email='user@test.com',
						password='1234'
					)),
					content_type='application/json'
			)
			data = json.loads(response.data.decode())
			self.assertTrue(data['status'] == 'error')
			self.assertTrue(data['message'] == 'User does not exist.')
			self.assertTrue(response.content_type == 'application/json')
			self.assertEqual(response.status_code, 404)

	def test_valid_logout(self):
		add_user('user', 'user@test.com', '1234')
		with self.client:
			# user login
			resp_login = self.client.post(
				'/auth/login',
				data=json.dumps(dict(
					email='user@test.com',
					password='1234'
				)),
				content_type='application/json'
			)
			# valid token logout
			response = self.client.get(
				'/auth/logout',
				headers=dict(
					Authorization='Bearer '+ json.loads(resp_login.data.decode()
					)['auth_token']
				)
			)
			data = json.loads(response.data.decode())
			self.assertTrue(data['status'] == 'success')
			self.assertTrue(data['message'] == 'Successfully logged out.')
			self.assertEqual(response.status_code, 200)

	def test_invalid_logout_expired_token(self):
		add_user('user', 'user@test.com', '1234')
		with self.client:
			# user login
			resp_login = self.client.post(
				'/auth/login',
				data=json.dumps(dict(
					email='user@test.com',
					password='1234'
				)),
				content_type='application/json'
			)
			# invalid token logout
			time.sleep(4)
			response = self.client.get(
				'/auth/logout',
				headers=dict(
					Authorization='Bearer '+ json.loads(resp_login.data.decode()
					)['auth_token']
				)
			)
			data = json.loads(response.data.decode())
			self.assertTrue(data['status'] == 'error')
			self.assertTrue(
				data['message'] ==
				'Signature expired. Please log in again.'
			)
			self.assertEqual(response.status_code, 401)

	def test_invalid_logout(self):
		with self.client:
			response = self.client.get(
				'/auth/logout',
				headers=dict(Authorization='Bearer invalid')
			)
			data = json.loads(response.data.decode())
			self.assertTrue(data['status'] == 'error')
			self.assertTrue(
				data['message'] ==
				'Invalid token. Please log in again.')
			self.assertEqual(response.status_code, 401)

	def test_invalid_logout_inactive(self):
		add_user('user', 'user@test.com', '1234')
		user = User.query.filter_by(email='user@test.com').first()
		user.active = False
		db.session.commit()
		with self.client:
			resp_login = self.client.post(
				'/auth/login',
				data=json.dumps(dict(
					email='user@test.com',
					password='1234'
				)),
				content_type='application/json'
			)
			response = self.client.get(
				'/auth/logout',
				headers=dict(
					Authorization='Bearer ' + json.loads(
						resp_login.data.decode()
						)['auth_token']
				)
			)
			data = json.loads(response.data.decode())
			self.assertTrue(data['status'] == 'error')
			self.assertTrue(
				data['message'] == 'Something went wrong. Please contact us.')
			self.assertEqual(response.status_code, 401)

	def test_user_status(self):
		add_user('user', 'user@test.com', '1234')
		with self.client:
			resp_login = self.client.post(
				'/auth/login',
				data=json.dumps(dict(
					email='user@test.com',
					password='1234'
				)),
				content_type='application/json'
			)
			response = self.client.get(
				'/auth/status',
				headers=dict(
					Authorization='Bearer '+ json.loads(resp_login.data.decode()
					)['auth_token']
				)
			)
			data = json.loads(response.data.decode())
			self.assertTrue(data['status'] == 'success')
			self.assertTrue(data['data'] is not None)
			self.assertTrue(data['data']['username'] == 'user')
			self.assertTrue(data['data']['email'] == 'user@test.com')
			self.assertTrue(data['data']['active'] is True)
			self.assertTrue(data['data']['created_at'])
			self.assertEqual(response.status_code, 200)

	def test_invalid_status(self):
		with self.client:
			response = self.client.get(
				'/auth/status',
				headers=dict(Authorization='Bearer invalid')
			)
			data = json.loads(response.data.decode())
			self.assertTrue(data['status'] == 'error')
			self.assertTrue(
				data['message'] ==
				'Invalid token. Please log in again.')
			self.assertEqual(response.status_code, 401)

	def test_invalid_status_inactive(self):
		add_user('user', 'user@test.com', '1234')
		user = User.query.filter_by(email='user@test.com').first()
		user.active = False
		db.session.commit()
		with self.client:
			resp_login = self.client.post(
				'/auth/login',
				data=json.dumps(dict(
					email='user@test.com',
					password='1234'
				)),
				content_type='application/json'
			)
			response = self.client.get(
				'/auth/status',
				headers=dict(
					Authorization='Bearer ' + json.loads(
						resp_login.data.decode()
						)['auth_token']
				)
			)
			data = json.loads(response.data.decode())
			self.assertTrue(data['status'] == 'error')
			self.assertTrue(
				data['message'] == 'Something went wrong. Please contact us.')
			self.assertEqual(response.status_code, 401)

	def test_add_user_inactive(self):
		add_user('user', 'user@test.com', '1234')
		user = User.query.filter_by(email='user@test.com').first()
		user.active = False
		db.session.commit()
		with self.client:
			resp_login = self.client.post(
				'/auth/login',
				data=json.dumps(dict(
					email='user@test.com',
					password='1234'
				)),
				content_type='application/json'
			)
			response = self.client.post(
				'/users',
				data=json.dumps(dict(
					username='user2',
					email='user2@test.com',
					password='1234'
				)),
				content_type='application/json',
				headers=dict(
					Authorization='Bearer ' + json.loads(
						resp_login.data.decode()
						)['auth_token']
				)
			)
			data = json.loads(response.data.decode())
			self.assertTrue(data['status'] == 'error')
			self.assertTrue(
				data['message'] == 'Something went wrong. Please contact us.')
			self.assertEqual(response.status_code, 401)
