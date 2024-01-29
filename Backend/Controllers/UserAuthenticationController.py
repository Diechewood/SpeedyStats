# UserAuthenticationController.py
from Services.UserAuthenticationService import UserAuthenticationService
from flask import Flask, request, jsonify

app = Flask(__name__)
auth_service = UserAuthenticationService()

@app.route('/register', methods=['POST'])
def register_user():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if auth_service.create_user(username, email, password):
        return jsonify({"message": "User registered successfully"}), 201
    else:
        return jsonify({"message": "Registration failed"}), 400

@app.route('/login', methods=['POST'])
def login_user():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if auth_service.verify_user(username, password):
        # Implement session management or token generation here
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401

if __name__ == '__main__':
    app.run(debug=True)
