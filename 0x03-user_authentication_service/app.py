#!/usr/bin/env python3
"""
Basic Flask app with a single route.
"""
from flask import Flask, jsonify

app = Flask(__name__)


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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
