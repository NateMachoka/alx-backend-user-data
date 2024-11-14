#!/usr/bin/env python3
""" Module of Session views
"""
from flask import request, jsonify, abort, make_response
from models.user import User
from api.v1.app import auth
from api.v1.views import app_views
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """Handles the login for session authentication"""
    email = request.form.get("email")
    password = request.form.get("password")

    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400

    # Retrieve the user instance using the email
    user_list = User.search({"email": email})
    user = user_list[0] if user_list else None
    if not user:
        return jsonify({"error": "no user found for this email"}), 404

    # Check if the password is correct
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    # Create a session ID for the user
    session_id = auth.create_session(user.id)
    response = jsonify(user.to_json())

    # Set the session cookie
    response.set_cookie(getenv("SESSION_NAME"), session_id)

    return response


@app_views.route(
    '/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def logout():
    """
    Handles logout for session authentication by deleting the session.
    """
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({}), 200
