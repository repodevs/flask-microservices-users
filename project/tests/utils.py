#!/usr/bin/env python
import datetime

from project import db
from project.api.models import User


def add_user(username, email, created_at=datetime.datetime.now()):
	user = User(username=username, email=email, created_at=created_at)
	db.session.add(user)
	db.session.commit()
	return user
