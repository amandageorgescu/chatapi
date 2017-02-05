#!/usr/local/bin/env python

import flask
import flask_sqlalchemy
import app
from app import db
from flask import json
from flask_testing import TestCase
import unittest

class Test(TestCase):

	def create_app(self):
		app.app.config['TESTING'] = True
		app.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
		db = flask_sqlalchemy.SQLAlchemy(app.app)
		self.baseURL = 'https://protected-beyond-84593.herokuapp.com'
		return app.app

	def setUp(self):
		db.create_all()

	def tearDown(self):
		db.session.remove()
		db.drop_all()

	# Application Util Tests
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

	# Route and Controller Tests
	def test_add_user_already_exists(self):
		user = app.User("Bob","bob@gmail.com")
		db.session.add(user)
		db.session.commit()
		response = self.client.post('/users', data='{"name":"Bob","email":"bob@gmail.com"}', content_type='application/json')
		self.assertEqual(json.loads(response.data).items(), {"status":"Error","message":"User with this email address already exists!"}.items())

	def test_add_user_name_too_long(self):
		response = self.client.post('/users', data='{"name":"Bobhghghjghjgjhghjghgjhghjghjghjghjghjghjghjghjghjgjhghjgjhghjghjghjghjghjghjgjhgjhhjghjghjgjghghjgjhgh","email":"bob@gmail.com"}', content_type='application/json')
		self.assertEqual(json.loads(response.data).items(), {"status":"Error","message":"Email and name cannot be more than 64 chars each!"}.items())

	def test_add_user_successful(self):
		response = self.client.post('/users', data='{"name":"Bob","email":"bob@gmail.com"}', content_type='application/json')
		self.assertEqual(json.loads(response.data).items(), {"status":"Success","message":"Congrats, Bob! You're now ready to chat!"}.items())

	def test_query_all_users_not_empty(self):
		user1 = app.User("Bob","bob@gmail.com")
		db.session.add(user1)
		user2 = app.User("Amanda Georgescu","georgescu.amanda@gmail.com")
		db.session.add(user2)
		db.session.commit()
		response = self.client.get('/users')
		self.assertEqual(json.loads(response.data).items(), {"status":"Success","Users":[{"name":"Bob","email":"bob@gmail.com"},{"name":"Amanda Georgescu","email":"georgescu.amanda@gmail.com"}]}.items())

	def test_query_all_users_empty(self):
		response = self.client.get('/users')
		self.assertEqual(json.loads(response.data).items(), {"status":"Error","message":"There is nobody to chat with yet!"}.items())

	def test_post_message_validation_error(self):
		response = self.client.post('/messages', data='{"sender":"georgescu.amanda@gmail.com","receiver":"bob@gmail.com","text":"Hey Bob"}', content_type='application/json')
		self.assertEqual(json.loads(response.data).items(), json.loads(app.validate_sender_and_receiver("georgescu.amanda@gmail.com","bob@gmail.com")).items())

	def test_post_message_too_long(self):
		user1 = app.User("Bob","bob@gmail.com")
		db.session.add(user1)
		user2 = app.User("Amanda Georgescu","georgescu.amanda@gmail.com")
		db.session.add(user2)
		db.session.commit()
		response = self.client.post('/messages', data='{"sender":"georgescu.amanda@gmail.com","receiver":"bob@gmail.com","text":"Hey Bob848748738497389748937djhfjdkhfjkdshfjkdhfjkhdjkfhjkdhfjkdhfjkhdjkhfjkdhfjkhdsjkfhjkdshfjkdhfjkhdsjhfhghghfdye5ruhfjhdfijdhsfksdjkfhdsjkfhjkdshfjkhdsjfkhsdkjhfjksdhfjkhdskjfhjksdhfjkhdsjkfhdsjkhfjksdhfjkhsdkjfhsdjkhfjkdshjkfhkjdshfjdshfjkhdsjkfhjkdshfjkhdsjkfhkjdshfjkdshfjkhdsjkhfkdshfjkdshfjkhdkjdhsfjkhdsjkfhjksdhfjdhsfjkhdsjkfhdskjhjkdshfjkhdskjfhjkdshfjkhsdjkfh"}', content_type='application/json')
		self.assertEqual(json.loads(response.data).items(), {"status":"Error","message":"Message is too long to send!"}.items())

	def test_post_message_successful(self):
		user1 = app.User("Bob","bob@gmail.com")
		db.session.add(user1)
		user2 = app.User("Amanda Georgescu","georgescu.amanda@gmail.com")
		db.session.add(user2)
		db.session.commit()
		response = self.client.post('/messages', data='{"sender":"georgescu.amanda@gmail.com","receiver":"bob@gmail.com","text":"Hey Bob"}', content_type='application/json')
		self.assertEqual(json.loads(response.data)["status"], "Success")
		self.assertEqual(json.loads(response.data)["message"]["name"], "Amanda Georgescu")
		self.assertEqual(json.loads(response.data)["message"]["text"], "Hey Bob")

	def test_get_message_validation_error(self):
		response = self.client.get('/messages', data='{"sender":"georgescu.amanda@gmail.com","receiver":"bob@gmail.com"}', content_type='application/json')
		self.assertEqual(json.loads(response.data).items(), json.loads(app.validate_sender_and_receiver("georgescu.amanda@gmail.com","bob@gmail.com")).items())

	def test_get_message_empty(self):
		user1 = app.User("Bob","bob@gmail.com")
		db.session.add(user1)
		user2 = app.User("Amanda Georgescu","georgescu.amanda@gmail.com")
		db.session.add(user2)
		db.session.commit()
		response = self.client.get('/messages', data='{"sender":"georgescu.amanda@gmail.com","receiver":"bob@gmail.com"}', content_type='application/json')
		self.assertEqual(json.loads(response.data), [])

	def test_get_message_successful_then_empty(self):
		user1 = app.User("Bob","bob@gmail.com")
		db.session.add(user1)
		user2 = app.User("Amanda Georgescu","georgescu.amanda@gmail.com")
		db.session.add(user2)
		message = app.Message("georgescu.amanda@gmail.com","bob@gmail.com","Hey Bob")
		db.session.add(message)
		db.session.commit()
		response = self.client.get('/messages', data='{"sender":"georgescu.amanda@gmail.com","receiver":"bob@gmail.com"}', content_type='application/json')
		self.assertEqual(json.loads(response.data)[0]["name"], "Amanda Georgescu")
		self.assertEqual(json.loads(response.data)[0]["text"], "Hey Bob")
		response = self.client.get('/messages', data='{"sender":"georgescu.amanda@gmail.com","receiver":"bob@gmail.com"}', content_type='application/json')
		self.assertEqual(json.loads(response.data), [])

	def test_get_message_correct_order(self):
		user1 = app.User("Bob","bob@gmail.com")
		db.session.add(user1)
		user2 = app.User("Amanda Georgescu","georgescu.amanda@gmail.com")
		db.session.add(user2)
		db.session.commit()
		self.client.post('/messages', data='{"sender":"georgescu.amanda@gmail.com","receiver":"bob@gmail.com","text":"Hey Bob"}', content_type='application/json')
		self.client.post('/messages', data='{"sender":"georgescu.amanda@gmail.com","receiver":"bob@gmail.com","text":"How are you?"}', content_type='application/json')
		response = self.client.get('/messages', data='{"sender":"georgescu.amanda@gmail.com","receiver":"bob@gmail.com"}', content_type='application/json')
		self.assertEqual(json.loads(response.data)[0]["text"], "Hey Bob")
		self.assertEqual(json.loads(response.data)[1]["text"], "How are you?")

if __name__ == '__main__':
    unittest.main()





