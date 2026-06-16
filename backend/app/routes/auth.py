from flask import Blueprint, request, jsonify
from ..services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    success = AuthService.register(data['username'], data['email'], data['password'])
    return jsonify({'success': success}), 201 if success else 400

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    user = AuthService.login(data['email'], data['password'])
    if user:
        return jsonify({'id': user['id'], 'username': user['username'], 'role': user['role']})
    return jsonify({'error': 'Invalid credentials'}), 401

@auth_bp.route('/profile/<int:user_id>', methods=['GET'])
def get_profile(user_id):
    user = AuthService.get_user_profile(user_id)
    if user:
        return jsonify({'id': user['id'], 'username': user['username'], 'email': user['email']})
    return jsonify({'error': 'User not found'}), 404
