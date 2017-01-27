#!/usr/local/bin/env python

import flask
import flask_sqlalchemy
import hashlib
import os
from flask import request, json

app = flask.Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/chat.db'
db = flask_sqlalchemy.SQLAlchemy(app)

#Model
class User(db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name = db.Column(db.String(64))
	email = db.Column(db.String(64))
	password = db.Column(db.String(64))

	def __init__(self, name=None, email=None, password=None):
		self.name = name
		self.email = email
		self.password = password

class Message(db.Model):
	__tablename__ = 'messages'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	sender = db.Column(db.String(64))
	receiver = db.Column(db.String(64))
	text = db.Column(db.String(256))
	delivered = db.Column(db.Integer)

	def __init__(self, sender=None, receiver=None, text=None, delivered=None):
		self.sender = sender
		self.receiver = receiver
		self.text = text
		self.delivered = delivered

#Routes
@app.route('/users', methods = ['POST', 'GET'])
def api_user():
	if request.method == 'POST':
		return add_user(request)
	if request.method == 'GET':
		return query_all_users(request)

@app.route('/messages', methods = ['POST', 'GET'])
def api_message():
	if request.method == 'POST':
		return post_message(request)
	if request.method == 'GET':
		return get_message(request)

#Controller
def add_user(request):
	user = User.query.filter(User.email == request.json['email']).first()
	if user != None:
		return "User with this email address already exists!\n"
	else:
		user = User(request.json['name'], request.json['email'])
		db.session.add(user)
		db.session.commit()
		return "Congrats, " + request.json['name'] + "! You're now ready to chat!\n"

def query_all_users(request):
	all_users = User.query.all()
	people_to_chat_with = "Here are some people you can chat with:\n"
	for user in all_users:
		user = user.name + " (" + user.email + ")\n"
		people_to_chat_with += user
	return people_to_chat_with

def post_message(request):
	message = Message(request.json['from'], request.json['to'], request.json['message'], 0)
	db.session.add(message)
	db.session.commit()
	sender_name = User.query.filter(User.email == request.json['from']).first()
	return sender_name.name + ": " + request.json['message'] + "\n"

def get_message(request):
	messages = Message.query.filter(Message.sender == request.json['from'] and Message.receiver == request.json['to'] and Message.delivered == 0).all()
	sender_name = User.query.filter(User.email == request.json['from']).first()
	unread_messages = ""
	for message in messages:
		if message.delivered != 1:
			unread_messages += sender_name.name + ": " + message.text + "\n"
			message.delivered = 1
	db.session.commit()
	return unread_messages	

if __name__ == '__main__':
	db.create_all()
	port = int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port=port)

