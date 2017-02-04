#!/usr/local/bin/env python

import flask
import flask_sqlalchemy
import app
from app import app, db
from app import json
from flask_testing import TestCase
import unittest

class Test(TestCase):

	def create_app(self):
		app.config['TESTING'] = True
		app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
		db = flask_sqlalchemy.SQLAlchemy(app)
		self.app = app.test_client()
		self.baseURL = 'https://protected-beyond-84593.herokuapp.com'
		return self.app

	def setUp(self):
		db.create_all()

	def tearDown(self):
		db.session.remove()
		db.drop_all()

	# Util Tests
	def test_validate_user_not_exists(self):
		exists = app.validate_user_exists("georgescu.amanda@gmail.com")
		self.assertEqual(exists, False)

	def test_validate_user_exists(self):
		user = app.User("Amanda Georgescu","georgescu.amanda@gmail.com")
		db.session.add(user)
		db.session.commit()
		exists = app.validate_user_exists("georgescu.amanda@gmail.com")
		self.assertEqual(exists, True)

	def test_validate_sender_not_exists(self):
		user = app.User("Bob","bob@gmail.com")
		db.session.add(user)
		db.session.commit()
		validation = app.validate_sender_and_receiver("georgescu.amanda@gmail.com", "bob@gmail.com")
		self.assertEqual(json.loads(validation).items(), {"status":"Error","message":"georgescu.amanda@gmail.com" + " is not registered to chat!"}.items())

	def test_validate_receiver_not_exists(self):
		user = app.User("Bob","bob@gmail.com")
		db.session.add(user)
		db.session.commit()
		validation = app.validate_sender_and_receiver("bob@gmail.com", "georgescu.amanda@gmail.com")
		self.assertEqual(json.loads(validation).items(), {"status":"Error","message":"georgescu.amanda@gmail.com" + " is not registered to chat!"}.items())

	def test_validate_sender_and_receiver_not_exist(self):
		validation = app.validate_sender_and_receiver("bob@gmail.com", "georgescu.amanda@gmail.com")
		self.assertEqual(json.loads(validation).items(), {"status":"Error","message":"bob@gmail.com" + " and " + "georgescu.amanda@gmail.com" + " are not registered to chat!"}.items())

	def test_validate_sender_and_receiver_exist(self):
		user1 = app.User("Bob","bob@gmail.com")
		db.session.add(user1)
		user2 = app.User("Amanda Georgescu","georgescu.amanda@gmail.com")
		db.session.add(user2)
		db.session.commit()
		validation = app.validate_sender_and_receiver("bob@gmail.com", "georgescu.amanda@gmail.com")
		self.assertEqual(validation, None)

	#Route and Controller Tests
	def test_add_user_already_exists(self):
		user = app.User("Bob","bob@gmail.com")
		db.session.add(user)
		db.session.commit()
		response = self.client.post('/users', data='{"name":"Bob","email":"bob@gmail.com"}', content_type='application/json')
		self.assertEqual(response, {"status":"Error","message":"User with this email address already exists!"})





if __name__ == '__main__':
    unittest.main()





