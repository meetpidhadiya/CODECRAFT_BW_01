# pip install flask

from flask import Flask, request, jsonify
import uuid
import re

app = Flask(__name__)

users = {}

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def is_valid_age(age):
    return isinstance(age, int) and 0 <= age <= 120

@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    age = data.get('age')

    if not name or not email or not age:
        return jsonify({'error': 'Missing required fields'}), 400
    if not is_valid_email(email):
        return jsonify({'error': 'Invalid email'}), 400
    if not is_valid_age(age):
        return jsonify({'error': 'Invalid age'}), 400

    user_id = str(uuid.uuid4())
    users[user_id] = {'id': user_id, 'name': name, 'email': email, 'age': age}
    return jsonify(users[user_id]), 201

@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(list(users.values())), 200

@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = users.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user), 200

@app.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    user = users.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    data = request.json
    name = data.get('name', user['name'])
    email = data.get('email', user['email'])
    age = data.get('age', user['age'])

    if email and not is_valid_email(email):
        return jsonify({'error': 'Invalid email'}), 400
    if age and not is_valid_age(age):
        return jsonify({'error': 'Invalid age'}), 400

    user.update({'name': name, 'email': email, 'age': age})
    return jsonify(user), 200

@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    if user_id not in users:
        return jsonify({'error': 'User not found'}), 404
    del users[user_id]
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
    
