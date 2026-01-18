"""
API endpoints for the application.
"""
from flask import Flask, request, jsonify
from auth import AuthManager
from user_service import UserService
from typing import Dict, Any

app = Flask(__name__)
auth_manager = AuthManager()
user_service = UserService()

def require_auth(f):
    """Decorator to require authentication for an endpoint."""
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        user_data = auth_manager.validate_token(token)
        if not user_data:
            return jsonify({'error': 'Unauthorized'}), 401
        request.user = user_data
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

@app.route('/api/users', methods=['POST'])
def create_user():
    """
    Create a new user.
    
    Expected JSON:
    {
        "username": "john_doe",
        "email": "john@example.com"
    }
    """
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No JSON data provided'}), 400
    
    username = data.get('username')
    email = data.get('email')
    
    if not username or not email:
        return jsonify({'error': 'Username and email are required'}), 400
    
    try:
        user = user_service.create_user(username, email)
        return jsonify({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'created_at': user.created_at.isoformat()
        }), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/users/<int:user_id>', methods=['GET'])
@require_auth
def get_user(user_id: int):
    """
    Get a user by ID (requires authentication).
    """
    user = user_service.get_user_by_id(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'created_at': user.created_at.isoformat()
    }), 200

@app.route('/api/users', methods=['GET'])
@require_auth
def list_users():
    """
    List all users (requires authentication).
    """
    users = user_service.list_all_users()
    return jsonify({
        'users': [{
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'created_at': user.created_at.isoformat()
        } for user in users]
    }), 200

@app.route('/api/auth/login', methods=['POST'])
def login():
    """
    Authenticate a user and get a token.
    
    Expected JSON:
    {
        "username": "john_doe",
        "password": "password123"
    }
    """
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No JSON data provided'}), 400
    
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400
    
    result = auth_manager.login(username, password)
    if result:
        token, user_data = result
        return jsonify({
            'token': token,
            'user': user_data
        }), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/api/auth/logout', methods=['POST'])
@require_auth
def logout():
    """
    Logout and invalidate token (requires authentication).
    """
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    if auth_manager.logout(token):
        return jsonify({'message': 'Logged out successfully'}), 200
    else:
        return jsonify({'error': 'Token not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)
