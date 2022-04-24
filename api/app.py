#Imports
from dataclasses import dataclass
from functools import wraps
import re
import time
import firebase_admin
from pyparsing import replaceWith
import pyrebase
import json
from firebase_admin import credentials, auth
from flask import Flask, request
import requests
#App configuration
app = Flask(__name__)
#Connect to firebase
cred = credentials.Certificate('./fbAdminConfig.json')
firebase = firebase_admin.initialize_app(cred)
pb = pyrebase.initialize_app(json.load(open('./fbconfig.json')))

#Data source
users = [{'uid': 1, 'name': 'test'}]

def check_token(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        if not request.headers.get('authorization'):
            return {'message': 'No token provided'},400
        try:
            user = auth.verify_id_token(request.headers['authorization'])
            request.user = user
        except Exception as exception:
            return {'message':f'Invalid token provided. {exception}'},400
        return f(*args, **kwargs)
    return wrap

#Api route to get users
@app.route('/api/userinfo')
@check_token
def userinfo():
    # get current user from firebase.auth
    user = request.user
    return user,200



@app.route('/api/upload', methods=['POST'])
@check_token
def upload():
    file = request.files['file']
    user = request.user
    if file is None:
        return {'message': 'Error missing file'},400
    if user is None:
        return {'message': 'Error not signed in'},401
    try:
        user_id = user['user_id']
        print(user)
        pb.storage().child(f'{user_id}').put(request.files['file'])
        return {'message': f'Successfully uploaded'},201
    except Exception as exception:
        # print the exception
        return {'message': f'Error uploading {exception} '},400
    

#Api route to sign up a new user
@app.route('/api/signup')
def signup():
    email = request.form.get('email')
    password = request.form.get('password')
    if email is None or password is None:
        return {'message': 'Error missing email or password'},400
    try:
        print(email, password)
        user = auth.create_user(
               email=email,
               password=password
        )
        return {'message': f'Successfully created user {user.uid}'},201
    except Exception as exception:
        # print the exception
        return {'message': f'Error creating user {exception} '},400


#Api route to get a new token for a valid user
@app.route('/api/token')
def token():
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        user = pb.auth().sign_in_with_email_and_password(email, password)
        jwt = user['idToken']
        return {'token': jwt}, 200
    except Exception as exception:
        # print the exception
        return {'message': f'There was an error logging in {exception}'},400


# api route to generate audio file from POST text and return it
@app.route('/api/generate', methods=['POST'])
@check_token
def generate():
    user = request.user
    text = request.form.get('text')
    if text is None:
        return {'message': 'Error missing text'},400
    if user is None:
        return {'message': 'Error not signed in'},401
    try:
        user_id = user['user_id']
        print(user)
        url = pb.storage().child(f'{user_id}').get_url()

        #fetch the file from firebase storage
        r = requests.get(url)
        
        if r.status_code == 200:
            return r.content, 200
        elif r.status_code == 404:
            return {'message': f'Error no voice sample file found for user {user_id}'},404
        else:
            return {'message': 'Error fetching file'},400

    except Exception as exception:
        # print the exception
        return {'message': f'Error generating: {exception} '},400

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)


