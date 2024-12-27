from flask import Flask
from flask import Blueprint, request, jsonify
from app.models.user import User, db
from sqlalchemy.exc import IntegrityError
from cerberus import Validator

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Needed for Flask-WTF CSRF protection

users_bp = Blueprint('user_routes', __name__)

registerSchema = {
    'firstName': {'type': 'string', 'minlength': 2, 'maxlength': 50, 'required': True},
    'lastName': {'type': 'string', 'minlength': 2, 'maxlength': 50, 'required': True},
    'email': {'type': 'string', 'regex': r'^[^@]+@[^@]+\.[^@]+$', 'required': True},
    'password': {'type': 'string', 'minlength': 8, 'maxlength': 50, 'required': True},
    'countryCode': {'type': 'string', 'minlength': 2, 'maxlength': 50, 'required': True},
    'mobileNo': {'type': 'integer', 'required': True},
    'empID': {'type': 'integer', 'required': True},
    'role': {'type': 'string', 'minlength': 2, 'maxlength': 50, 'required': True},
    'userType': {'type': 'string', 'allowed': ['user', 'master_admin'], 'required': True},
}

validator = Validator(registerSchema)

# CREATE user
@users_bp.route('/register', methods=['POST'])
def create_user():
    data = request.get_json()
    if not validator.validate(data):
        return jsonify({"errors": validator.errors}), 400
    print("data",data)

    return jsonify({"message": "User registered successfully", "data": data}), 200

# READ all users
@users_bp.route('/users', methods=['GET'])
def get_users():
    0
    
    users = User.query.all()
    users_list = [{"id": user.id, "name": user.name, "email": user.email} for user in users]
    return jsonify(users_list)

# READ a single user
@users_bp.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({"id": user.id, "name": user.name, "email": user.email})

# UPDATE user
@users_bp.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.get_json()
    
    

    user = User.query.get(id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    user.name = data.get('name', user.name)
    user.email = data.get('email', user.email)
    user.password = data.get('password', user.password)
    
    db.session.commit()
    return jsonify({"message": "User updated"})

# DELETE user
@users_bp.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted'}), 200


