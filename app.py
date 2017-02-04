#!/usr/local/bin/env python

import flask
import flask_sqlalchemy
import hashlib
import app
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
	def __init__(self, name=None, email=None):
		self.name = name
		self.email = email

class Message(db.Model):
	__tablename__ = 'messages'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	sender = db.Column(db.String(64))
	receiver = db.Column(db.String(64))
	text = db.Column(db.String(256))
	#TODO: Add time stamp
	delivered = db.Column(db.Integer)

	def __init__(self, sender=None, receiver=None, text=None, delivered=None):
		self.sender = sender
		self.receiver = receiver
		self.text = text
		self.delivered = delivered

#Util
def validate_user_exists(email_address):
	user = User.query.filter(User.email == email_address).first()
	if user != None:
		return True
	else:
		return False

def validate_sender_and_receiver(sender_email, receiver_email):
	sender_valid = validate_user_exists(sender_email)
	receiver_valid = validate_user_exists(receiver_email)
	if sender_valid and receiver_valid:
		return None
	elif sender_valid and not receiver_valid:
		return json.dumps({"status":"Error","message":receiver_email + " is not registered to chat!"})
	elif not sender_valid and receiver_valid:
		return json.dumps({"status":"Error","message":sender_email + " is not registered to chat!"})
	else:
		return json.dumps({"status":"Error","message":sender_email + " and " + receiver_email + " are not registered to chat!"})

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
	if validate_user_exists(request.json['email']):
		return json.dumps({"status":"Error","message":"User with this email address already exists!"})
	elif len(request.json['email']) > 64 or len(request.json['name']) > 64:
		return json.dumps({"status":"Error","message":"Email and name cannot be more than 64 chars each!"})
	else:
		user = User(request.json['name'], request.json['email'].lower())
		db.session.add(user)
		db.session.commit()
		return json.dumps({"status":"Success","message":"Congrats, " + request.json['name'] + "! You're now ready to chat!"})

def query_all_users(request):
	all_users = User.query.all()
	people_to_chat_with = []
	for user in all_users:
		user = {"name":user.name,"email":user.email}
		people_to_chat_with.append(user)
	if len(people_to_chat_with) != 0:
		return json.dumps(people_to_chat_with)
	else:
		return json.dumps({"status":"Error","message":"There is nobody to chat with yet!"})

def post_message(request):
	validation_error = validate_sender_and_receiver(request.json['sender'], request.json['receiver'])
	if validation_error == None:
		if len(request.json['text']) > 256:
			return json.dumps({"status":"Error","message":"Message is too long to send!"})
		else:
			message = Message(request.json['sender'], request.json['receiver'], request.json['text'], 0)
			db.session.add(message)
			db.session.commit()
			sender = User.query.filter(User.email == request.json['sender']).first()
			return json.dumps({"name":sender.name,"text":request.json['text']})
	else:
		return validation_error

def get_message(request):
	validation_error = validate_sender_and_receiver(request.json['sender'], request.json['receiver'])
	if validation_error == None:
		messages = Message.query.filter(Message.sender == request.json['sender'] and Message.receiver == request.json['receiver'] and Message.delivered == 0).all()
		sender = User.query.filter(User.email == request.json['sender']).first()
		unread_messages = []
		for message in messages:
			if message.delivered != 1:
				unread_messages.append({"name":sender.name,"text":message.text})
				message.delivered = 1
		db.session.commit()
		return json.dumps(unread_messages)	
	else:
		return validation_error

if __name__ == '__main__':
	db.create_all()
	port = int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port=port)




