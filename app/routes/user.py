from flask import Flask
from flask import Blueprint, request, jsonify
from app.models.user import User, db
from sqlalchemy.exc import IntegrityError
from cerberus import Validator
from werkzeug.security import generate_password_hash
from .token import verifyJWTToken

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
    'empID': {'type': 'string', 'required': True},
    'role': {'type': 'string', 'minlength': 2, 'maxlength': 50, 'required': True},
}

validator = Validator(registerSchema)
# CREATE user
@users_bp.route('/register', methods=['POST'])
def create_user():
    data = request.get_json()
    if not validator.validate(data):
        return jsonify({"errors": validator.errors}), 400
    data['password'] = generate_password_hash(data['password'])
    new_user = User(**data) 
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"message": "User registered successfully", "data": data}), 200

# READ all users 
@users_bp.route('/users', methods=['GET'])
def get_users():
    # Get pagination parameters from the request
    page = request.args.get('page', default=1, type=int)  # Default page is 1
    per_page = request.args.get('per_page', default=10, type=int)  # Default items per page is 10

    # Fetch paginated users from the database
    paginated_users = User.query.paginate(page=page, per_page=per_page, error_out=False)

    # Serialize the user data into dictionaries
    users_list = [
        {
            "id": user.id,
            "firstName": user.firstName,
            "lastName": user.lastName,
            "email": user.email,
            "role": user.role,
            "mobileNo": user.mobileNo,
            "is_blocked": user.is_blocked,
            "status": user.status,
            "created_at": user.created_at,
            "updated_at": user.updated_at,
        }
        for user in paginated_users.items
    ]

    return jsonify({
        "message": "Users fetched successfully",
        "data": users_list,
        "pagination": {
            "page": paginated_users.page,
            "per_page": paginated_users.per_page,
            "total_pages": paginated_users.pages,
            "total_items": paginated_users.total,
        }
    }), 200



@users_bp.route('/<int:id>', methods=['GET'])
@verifyJWTToken(['master_admin', 'user'])
def get_user(id):
    user = User.query.filter_by(id=id).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Serialize the user data into a dictionary, excluding userType
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

    # Return the serialized user data
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
    user.password = data.get('password', user.password)  # Be cautious about updating password
    user.role = data.get('role', user.role)  # Optional: update role if provided
    user.status = data.get('status', user.status)  # Optional: update status if provided
    user.is_blocked = data.get('is_blocked', user.is_blocked)  # Optional: update block status

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

