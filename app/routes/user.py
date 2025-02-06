from sqlalchemy import or_
from flask import Flask
from flask import Blueprint, request, jsonify
from app.models.user import User, db
from sqlalchemy.exc import IntegrityError
from cerberus import Validator
from werkzeug.security import generate_password_hash
from .token import verifyJWTToken, check_permissions
from .logs import addLogsActivity
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'


users_bp = Blueprint('user_routes', __name__)

registerSchema = {
    'firstName': {'type': 'string', 'minlength': 2, 'maxlength': 50, 'required': True},
    'lastName': {'type': 'string', 'minlength': 2, 'maxlength': 50, 'required': True},
    'email': {'type': 'string', 'regex': r'^[^@]+@[^@]+\.[^@]+$', 'required': True},
    'password': {'type': 'string', 'minlength': 8, 'maxlength': 50, 'required': True},
    'countryCode': {'type': 'string', 'minlength': 2, 'maxlength': 50, 'required': True},
    'mobileNo': {'type': 'integer', 'required': True},
    'empID': {'type': 'string', 'required': True},
    'role_id': {'type': 'integer', 'required': True},
}

validator = Validator(registerSchema)
# CREATE user


@users_bp.route('/register', methods=['POST'])
@verifyJWTToken(['master_admin'])
def create_user():
    data = request.get_json()
    if not validator.validate(data):
        addLogsActivity(request, 'Register', 'registration unsuccessfully')
        return jsonify({"errors": validator.errors}), 400

    data['password'] = generate_password_hash(data['password'])
    try:
        new_user = User(**data)
        db.session.add(new_user)
        db.session.commit()
        user_data = {
            "id": new_user.id,
            "firstName": new_user.firstName,
            "lastName": new_user.lastName,
            "email": new_user.email,
            "mobileNo": new_user.mobileNo,
        }
        addLogsActivity(request, 'Register', 'registration successfully')

        return jsonify({"message": "User registered successfully", "data": user_data}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An error occurred while creating the user.", "details": str(e)}), 500


# READ all users for master_admin
@users_bp.route('/all', methods=['GET'])
@verifyJWTToken(['master_admin'])
def get_users():
    # Get the search value from the request
    search_val = request.args.get('searchVal', default=None, type=str)
    role_ids = request.args.get('roleIds', default=None, type=str)

    # Start building the query
    query = User.query

    # If a search value exists, filter across multiple fields
    if search_val:
        search_val = search_val.strip().lower()  # Normalize input (trim and lowercase)
        search_filter = or_(
            User.firstName.ilike(f'%{search_val}%'),
            User.lastName.ilike(f'%{search_val}%'),
            User.email.ilike(f'%{search_val}%'),
            User.mobileNo.ilike(f'%{search_val}%')
        )
        query = query.filter(search_filter)

    # Apply role filtering if role_ids exist
    if role_ids:
        role_ids_list = [int(id) for id in role_ids.split(',')]
        query = query.filter(User.role_id.in_(role_ids_list))

    # Debugging: Print the SQL query for troubleshooting
    # print("Generated SQL Query:", str(query))

    # Fetch users based on the query
    users = query.all()
    if not users:
        return jsonify({
            "message": "No data found matching the search criteria.",
            "total_items": 0
        }), 404  # 404 Not Found status code


    # Serialize user data into dictionaries
    users_list = [
        {
            "id": user.id,
            "firstName": user.firstName,
            "lastName": user.lastName,
            "email": user.email,
            "roleId": user.role.id,
            "mobileNo": user.mobileNo,
            "is_blocked": user.is_blocked,
            "status": user.status,
            "created_at": user.created_at,
            "updated_at": user.updated_at,
        }
        for user in users
    ]

    # Return the response
    return jsonify({
        "message": "Users fetched successfully",
        "data": users_list,
        "total_items": len(users_list)
    }), 200


@users_bp.route('/<int:id>', methods=['GET'])
@verifyJWTToken(['master_admin', 'user'])
@check_permissions(['read-user'])
def get_user(id):

    user = User.query.filter_by(id=id).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    role_data = {
        "id": user.role.id,
        "name": user.role.name,
        "permissions": [
            {"id": perm.id, "slug": perm.slug} for perm in user.role.permissions
        ] if user.role.permissions else None
    } if user.role else None
    user_data = {
        "id": user.id,
        "firstName": user.firstName,
        "lastName": user.lastName,
        "email": user.email,
        "role": role_data,
        "mobileNo": user.mobileNo,
        "is_blocked": user.is_blocked,
        "status": user.status,
        "created_at": user.created_at,
        "updated_at": user.updated_at,
        # "notifications": notifications_data
    }
    return jsonify({"message": "User fetched successfully", "data": user_data}), 200

# UPDATE user


@users_bp.route('/users/<int:id>', methods=['PUT'])
@verifyJWTToken(['master_admin'])
def update_user(id):
    # Get the input data from the request body
    data = request.get_json()

    # Validate if the necessary data is provided (you can adjust the fields to be required)
    if not data:
        return jsonify({'error': 'No input data provided'}), 400

    # Fetch the user by ID
    user = User.query.filter_by(id=id).first()

    # If user not found, return a 404 error
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Update the user fields with the provided data or keep existing values if no new data is provided
    user.firstName = data.get('firstName', user.firstName)
    user.lastName = data.get('lastName', user.lastName)
    user.countryCode = data.get('countryCode', user.countryCode)
    user.mobileNo = data.get('mobileNo', user.mobileNo)
    user.email = data.get('email', user.email)
    # Be cautious about updating password
    user.password = data.get('password', user.password)
    # Optional: update role if provided
    user.role = data.get('role', user.role)
    # Optional: update status if provided
    user.status = data.get('status', user.status)
    # Optional: update block status
    user.is_blocked = data.get('is_blocked', user.is_blocked)

    # Commit the changes to the database
    db.session.commit()

    # Return the updated user data in the response
    user_data = {
        "id": user.id,
        "firstName": user.firstName,
        "lastName": user.lastName,
        "email": user.email,
        "role": user.role,
        "mobileNo": user.mobileNo,
        "is_blocked": user.is_blocked,
        "status": user.status,
        "created_at": user.created_at,
        "updated_at": user.updated_at
    }

    # Return a success message along with the updated user data
    return jsonify({"message": "User updated successfully", "data": user_data}), 200

# DELETE user


@users_bp.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.filter_by(id=id).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted'}), 200

# UPDATE user


@users_bp.route('/block/<int:id>', methods=['POST'])
@verifyJWTToken(['master_admin'])
def block_user(id):
    # Get the input data from the request body
    data = request.get_json()

    # Validate if the necessary data is provided (you can adjust the fields to be required)
    if not data:
        return jsonify({'error': 'No input data provided'}), 400

    # Fetch the user by ID
    user = User.query.filter_by(id=id).first()

    # If user not found, return a 404 error
    if not user:
        return jsonify({'error': 'User not found'}), 404
    if user.userType == 'master_admin':
        return jsonify({'error': 'Master admin can not be block'}), 404
    if user.is_blocked == True:
        return jsonify({'error': 'User Already Blocked'}), 404

    user.status = data.get('status', False)
    user.is_blocked = data.get('is_blocked', True)

    db.session.commit()

    return jsonify({"message": "User blocked successfully"}), 200
