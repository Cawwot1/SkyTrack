from flask import Flask, request, jsonify, make_response, abort
from flask_sqlalchemy import SQLAlchemy
import os
from flask_cors import CORS
from auth import user_auth_register, user_auth_login, user_auth_logout, user_auth_validate_token
from forum import user_create_forum, user_add_reply
from data import admin_retrieve_forum_data
import re
from asyncio import *

# Regex pattern to validate inputs
PATTERN = re.compile(r'^[a-zA-Z0-9_]+$')

# Regex pattern to validate email
EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9_]+@+.')

# Regex pattern to validate password
PASSWORD_PATTERN = re.compile(r'^[a-zA-Z0-9_]')

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent XXS and JS 
app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'  # Helps prevent CSRF attacks from different sites

CORS(app, supports_credentials=True, origins=["http://127.0.0.1:3001"])

@app.route('/') 
async def index():
    return 'Index route'

@app.route('/auth/register', methods=['POST', 'GET'])
async def register_user():
    print(1)
    # Retrieving input
    data = request.json
    email = data['email']
    password = data['password']
    first_name = data['firstName']
    last_name = data['lastName']

    # Input validation and sanitisation
    if not email or not password or not first_name or not last_name:
        return jsonify({'error': 'All fields are required'}), 400
    if len(email) > 100:
        return jsonify({'error': 'Email cannot have over 100 characters'}), 400
    if len(first_name) > 100:
        return jsonify({'error': 'First name cannot have over 100 characters'}), 400
    if len(last_name) > 100:
        return jsonify({'error': 'Last name cannot have over 100 characters'}), 400
    if len(password) > 20:
        return jsonify({'error': 'Password cannot have over 20 characters'}), 400
    if not PATTERN.match(first_name) or not PATTERN.match(last_name):
        return jsonify({'error': 'Invalid first/last name format.'}), 400
    if not PASSWORD_PATTERN.match(password):
        return jsonify({'error': 'Invalid password format.'}), 400
    if not EMAIL_PATTERN.match(email):
        return jsonify({'error': 'Invalid email format.'}), 400

    password = re.escape(password)
    email = re.escape(email)
    first_name = re.escape(first_name)
    last_name = re.escape(last_name)
    print(3)

    try:
        # Generating session/CSRF token and passing them to frontend
        print(4)
        session_token, csrf_token = await user_auth_register(email, password, first_name, last_name)
        print(5)
        response = make_response(jsonify({"message": "User registered successfully",
                                          "csrf_token": csrf_token}), 201)
        print(6)
        response.set_cookie('session_token', session_token, httponly=True, secure=True)
        print(7)
        return response
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return jsonify({"error": str(e)}), 406

@app.route('/auth/login', methods=['POST'])
async def login_user():
    data = request.json
    email = data['email']
    password = data['password']

    # Input validation and sanitisation
    if not email or not password:
        return jsonify({'error': 'All fields are required'}), 400
    if len(email) > 100:
        return jsonify({'error': 'Email cannot have over 100 characters'}), 400
    if len(password) > 20:
        return jsonify({'error': 'Password cannot have over 20 characters'}), 400
    if not PASSWORD_PATTERN.match(password):
        return jsonify({'error': 'Invalid password format.'}), 400
    if not EMAIL_PATTERN.match(email):
        return jsonify({'error': 'Invalid email format.'}), 400
    password = re.escape(password)
    email = re.escape(email)

    try:
        # Generating session/CSRF token and passing them to frontend
        session_token, csrf_token = await user_auth_login(email, password)
        response = make_response(jsonify({"message": "User logged in successfully",
                                          "csrf_token": csrf_token}), 201)
        response.set_cookie('session_token', session_token, httponly=True, secure=True)
        return response
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return jsonify({"error": str(e)}), 401

@app.route('/auth/logout', methods=['DELETE'])
async def logout_user():
    data = request.json
    session_token = request.cookies.get('session_token')
    csrf_token = data['csrfToken']

    try:
        await user_auth_logout(session_token, csrf_token)
        response = make_response(jsonify({"message": "User logged out successfully"}), 201)
        response.set_cookie('session_token', 'to_delete', max_age=0)
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return jsonify({"error": str(e)}), 401

@app.route('/forum/new/question', methods=['POST']) 
async def create_new_forum():
    data = request.json
    forum_title = data['title']
    forum_question = data['forumQuestion']
    session_token = request.cookies.get('session_token')
    csrf_token = data['csrfToken']

    # Input validation and sanitisation
    if not forum_question or not forum_title:
        return jsonify({'error': 'All fields are required'}), 400
    if len(forum_title) > 100:
        return jsonify({'error': 'Forum title cannot have over 100 characters'}), 400
    if len(forum_question) > 500:
        return jsonify({'error': 'Question cannot have over 500 characters'}), 400
    if not PATTERN.match(forum_title):
        return jsonify({'error': 'Invalid forum title format.'}), 400
    if not PATTERN.match(forum_question):
        return jsonify({'error': 'Invalid forum question format.'}), 400
    forum_title = re.escape(forum_title)
    forum_question = re.escape(forum_question)

    try:
        await user_create_forum(forum_title, forum_question, session_token, csrf_token)
        return jsonify({"message": "Forum created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 401

@app.route('/forum/retrieve', methods=['GET']) 
async def retrieve_all_forums():
    try:
        forum_dict = await admin_retrieve_forum_data()
        return jsonify({"message": "All forum data returned successfully", 
                        "forums": forum_dict}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 401

@app.route('/auth/validate', methods=['POST'])
async def validate_token():
    data = request.json
    session_token = request.cookies.get('session_token')
    csrf_token = data['csrfToken']

    try:
        if (await user_auth_validate_token(session_token, csrf_token)):
            return jsonify({"message": "Token is valid"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 401

@app.route('/forum/reply/submit', methods=['POST'])
async def store_reply():
    data = request.json
    forum_id = data['forumId']
    reply_comment = data['reply']
    session_token = request.cookies.get('session_token')
    csrf_token = data['csrfToken']

    # Input validation and sanitisation
    if not forum_id or not reply_comment:
        return jsonify({'error': 'All fields are required'}), 400
    if len(reply_comment) > 500:
        return jsonify({'error': 'Reply cannot have over 500 characters'}), 400
    if not type(forum_id) == int:
        return jsonify({'error': 'Invalid forum id format.'}), 400
    if not PATTERN.match(reply_comment):
        return jsonify({'error': 'Invalid reply comment format.'}), 400
    reply_comment = re.escape(reply_comment)

    try:
        await user_add_reply(forum_id, reply_comment, session_token, csrf_token)
        return jsonify({"message": "Forum reply added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 401

if __name__ == '__main__':
    app.run(debug=True, port=5005)