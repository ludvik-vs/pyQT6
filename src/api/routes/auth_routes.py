from flask import Blueprint, request, jsonify
from src.services.auth_service import AuthService
from src.db.db_operations.db_user import DatabaseUser

auth_bp = Blueprint('auth', __name__)
db_manager = DatabaseUser()
auth_service = AuthService(db_manager)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'message': 'Missing username or password'}), 400
    
    user = auth_service.authenticate(username, password)
    if user:
        return jsonify({
            'success': True,
            'user': {
                'id': user.user_id,
                'username': user.username,
                'role': user.role
            }
        })
    
    return jsonify({'message': 'Invalid credentials'}), 401

@auth_bp.route('/users', methods=['GET'])
def get_users():
    users = auth_service.get_all_users()
    return jsonify({'users': users})

@auth_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role', 'user')
    
    if not username or not password:
        return jsonify({'message': 'Missing required fields'}), 400
    
    success = auth_service.register_user(username, password, role)
    if success:
        return jsonify({'message': 'User created successfully'}), 201
    return jsonify({'message': 'Username already exists'}), 409

@auth_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    success = auth_service.update_user(
        user_id,
        new_username=data.get('username'),
        new_password=data.get('password'),
        new_role=data.get('role')
    )
    if success:
        return jsonify({'message': 'User updated successfully'})
    return jsonify({'message': 'User update failed'}), 400

@auth_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    success = auth_service.delete_user(user_id)
    if success:
        return jsonify({'message': 'User deleted successfully'})
    return jsonify({'message': 'User deletion failed'}), 400