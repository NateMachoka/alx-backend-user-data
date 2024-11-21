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

@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """
    DELETE /sessions route to log out the user.

    Expected:
        - The request must contain the session ID as a cookie with the key "session_id".

    Behavior:
        - If a valid session exists, destroy it and redirect to GET /.
        - If no valid session exists, respond with a 403 HTTP status.

    Returns:
        - A redirection to the root route if successful.
        - A 403 error if the session ID is invalid.
    """
    session_id = request.cookies.get('session_id')

    if not session_id:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)

    # Destroy the session
    AUTH.destroy_session(user.id)

    # Redirect to the root route
    response = make_response('', 302)
    response.headers['Location'] = '/'
    return response


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    """
    GET /profile route to retrieve the user's profile information.

    Expected:
        - The request must contain the session ID as a cookie.

    Behavior:
        - If a valid session, respond user's email and a 200 HTTP status.
        - If not valid session, respond with a 403 HTTP status.

    Returns:
        - JSON payload with the user's email if the session is valid.
        - A 403 error if the session is invalid.
    """
    session_id = request.cookies.get('session_id')

    if not session_id:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)

    return jsonify({"email": user.email}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
