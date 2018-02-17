#!/usr/bin/env python
from project import db
from project.api.models import User
from project.tests.base import BaseTestCase
from sqlalchemy.exc import IntegrityError
from project.tests.utils import add_user


class TestUserModel(BaseTestCase):
    
    def test_add_user(self):
        """Ensure a new user can be added to the database"""
        user = add_user('testuser', 'user@test.com', 'test')
        self.assertTrue(user.id)
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'user@test.com')
        self.assertTrue(user.active)
        self.assertTrue(user.created_at)

    def test_add_user_duplicate_username(self):
        """Ensure error is thrown if the username already exists"""
        add_user('testuser', 'user@test.com', 'test')
        duplicate_user = User(
            username='testuser',
            email='user2@test.com',
            password='password2'
        )
        db.session.add(duplicate_user)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_add_user_duplicate_email(self):
        """Ensure error is thrown if the email already exists"""
        add_user('testuser', 'user@test.com', 'test')
        duplicate_user = User(
            username='testuser2',
            email='user@test.com',
            password='password2'
        )
        db.session.add(duplicate_user)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_password_are_random(self):
        user_one = add_user('user', 'user@test.com', 'test')
        user_two = add_user('user2', 'user2@test.com', 'test2')
        self.assertNotEqual(user_one.password, user_two.password)

    def test_encode_auth_token(self):
        user = add_user('testuser', 'user@test.com', 'password')
        auth_token = user.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, bytes))

    def test_decode_auth_token(self):
        user = add_user('testuser', 'user@test.com', 'password')
        auth_token = user.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, bytes))
        self.assertTrue(User.decode_auth_token(auth_token), user.id)
