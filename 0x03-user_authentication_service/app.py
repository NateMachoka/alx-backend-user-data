#!/usr/bin/env python3
"""
Basic Flask app with a single route.
"""
from flask import Flask, jsonify, request, abort, make_response
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"])
def welcome():
    """
    Root route returning a welcome message.
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users() -> str:
    """
    POST /users route to register a new user.

    Expected form data:
        - email: User's email address
        - password: User's password

    Returns:
        - JSON payload with a success or error message.
    """
    try:
        email = request.form.get('email', None)
        password = request.form.get('password', None)
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"}), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400



@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """
    POST /sessions route to log in the user and create a session.

    Expected form data:
        - email: User's email address
        - password: User's password

    Returns:
        - JSON payload with the session ID if the login is successful.
        - Abort with 401 if login information is incorrect.
    """
    email = request.form.get('email')
    password = request.form.get('password')

    # Check if the login credentials are valid
    if not AUTH.valid_login(email, password):
        abort(401)

    session_id = AUTH.create_session(email)
    response = make_response(jsonify({"email": email, "message": "logged in"}))
    response.set_cookie('session_id', session_id)

    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
