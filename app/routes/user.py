from sqlalchemy import or_
from flask import Flask
from flask import Blueprint, request, jsonify
from app.models.user import User, db
from sqlalchemy.exc import IntegrityError
from cerberus import Validator
from werkzeug.security import generate_password_hash
from .token import verifyJWTToken, check_permissions
from .logs import addLogsActivity
from ..helper.response import success_response, error_response

app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key"


users_bp = Blueprint("user_routes", __name__)

registerSchema = {
    "firstName": {"type": "string", "minlength": 2, "maxlength": 50, "required": True},
    "lastName": {"type": "string", "minlength": 2, "maxlength": 50, "required": True},
    "email": {"type": "string", "regex": r"^[^@]+@[^@]+\.[^@]+$", "required": True},
    "password": {"type": "string", "minlength": 8, "maxlength": 50, "required": True},
    "countryCode": {
        "type": "string",
        "minlength": 2,
        "maxlength": 50,
        "required": True,
    },
    "mobileNo": {"type": "integer", "required": True},
    "empID": {"type": "string", "required": True},
    "role_id": {"type": "integer", "required": True},
}

validator = Validator(registerSchema)


# CREATE User
@users_bp.route("/register", methods=["POST"])
@verifyJWTToken(["master_admin"])
def create_user():
    data = request.get_json()
    if not validator.validate(data):
        addLogsActivity(request, "Register", "registration unsuccessfully")
        return error_response("Input validation failed", str(validator.errors), 400)

    data["password"] = generate_password_hash(data["password"])
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
        addLogsActivity(request, "Register", "registration successfully")
        return success_response(user_data, "User registered successfully", 200)
    except Exception as e:
        db.session.rollback()
        return error_response("Failed to create user", str(e), 500)


# READ all users for master_admin
@users_bp.route("/all", methods=["GET"])
@verifyJWTToken(["master_admin"])
def get_users():
    try:
        page = request.args.get("page", default=1, type=int)
        per_page = request.args.get("per_page", default=10, type=int)
        search_val = request.args.get("searchVal", default=None, type=str)
        role_ids = request.args.get("roleIds", default=None, type=str)

        query = User.query

        # If a search value exists, filter across multiple fields
        if search_val:
            search_val = (
                search_val.strip().lower()
            )  # Normalize input (trim and lowercase)
            search_filter = or_(
                User.firstName.ilike(f"%{search_val}%"),
                User.lastName.ilike(f"%{search_val}%"),
                User.email.ilike(f"%{search_val}%"),
                User.mobileNo.ilike(f"%{search_val}%"),
            )
            query = query.filter(search_filter)

        # Apply role filtering if role_ids exist
        if role_ids:
            role_ids_list = [int(id) for id in role_ids.split(",")]
            query = query.filter(User.role_id.in_(role_ids_list))

        # Apply pagination
        paginated_users = query.paginate(page=page, per_page=per_page, error_out=False)

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
            for user in paginated_users.items
        ]
        # Return the response
        return success_response(
            users_list,
            "Users fetched successfully",
            200,
            {
                "total_items": paginated_users.total,
                "total_pages": paginated_users.pages,
                "current_page": paginated_users.page,
                "per_page": paginated_users.per_page,
            }
        )
    except Exception as e:

        return error_response("Failed to fetch users", str(e), 500)


@users_bp.route("/<int:id>", methods=["GET"])
@verifyJWTToken(["master_admin", "user"])
@check_permissions(["read-user"])
def get_user(id):
    try:
        user = User.query.filter_by(id=id).first()
        if not user:
            return error_response("User not found", "User not found", 404)

        role_data = (
            {
                "id": user.role.id,
                "name": user.role.name,
                "permissions": (
                    [
                        {"id": perm.id, "slug": perm.slug}
                        for perm in user.role.permissions
                    ]
                    if user.role.permissions
                    else None
                ),
            }
            if user.role
            else None
        )
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
        return success_response(user_data, "Users fetched successfully", 200)

    except Exception as e:
        return error_response("Failed to fetch user", str(e), 500)


# UPDATE user


@users_bp.route("/users/<int:id>", methods=["PUT"])
@verifyJWTToken(["master_admin"])
def update_user(id):
    # Get input data from request
    data = request.get_json()

    if not data:
        addLogsActivity(
            request, "Update", "Update unsuccessful - No input data provided"
        )
        return error_response("Update failed", "No input data provided", 400)

    try:
        # Fetch user by ID
        user = User.query.filter_by(id=id).first()

        if not user:
            addLogsActivity(request, "Update", "Update unsuccessful - User not found")
            return error_response(
                "User not found", "No user exists with the given ID", 404
            )

        # Update user fields
        user.firstName = data.get("firstName", user.firstName)
        user.lastName = data.get("lastName", user.lastName)
        user.countryCode = data.get("countryCode", user.countryCode)
        user.mobileNo = data.get("mobileNo", user.mobileNo)
        user.email = data.get("email", user.email)

        # Update password only if a new one is provided
        if "password" in data:
            user.password = generate_password_hash(data["password"])

        user.role = data.get("role", user.role)
        user.status = data.get("status", user.status)
        user.is_blocked = data.get("is_blocked", user.is_blocked)

        # Commit changes to DB
        db.session.commit()

        # Construct response data
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
            "updated_at": user.updated_at,
        }

        addLogsActivity(request, "Update", "User updated successfully")
        return success_response(user_data, "User updated successfully", 200)

    except Exception as e:
        db.session.rollback()
        addLogsActivity(
            request, "Update", "Update unsuccessful - Internal server error"
        )
        return error_response("Failed to update user", str(e), 500)


@users_bp.route("/users/<int:id>", methods=["DELETE"])
@verifyJWTToken(["master_admin"])
def delete_user(id):
    try:
        # Fetch user by ID
        user = User.query.filter_by(id=id).first()

        if not user:
            addLogsActivity(request, "Delete", "Delete unsuccessful - User not found")
            return error_response(
                "User not found", "No user exists with the given ID", 404
            )

        db.session.delete(user)
        db.session.commit()

        addLogsActivity(request, "Delete", "User deleted successfully")
        return success_response({}, "User deleted successfully", 200)

    except Exception as e:
        db.session.rollback()
        addLogsActivity(
            request, "Delete", "Delete unsuccessful - Internal server error"
        )
        return error_response("Failed to delete user", str(e), 500)


@users_bp.route("/block/<int:id>", methods=["POST"])
@verifyJWTToken(["master_admin"])
def block_user(id):
    try:
        # Get the input data from request
        data = request.get_json()

        if not data:
            addLogsActivity(
                request, "Block", "Block unsuccessful - No input data provided"
            )
            return error_response("Block failed", "No input data provided", 400)

        # Fetch user by ID
        user = User.query.filter_by(id=id).first()

        if not user:
            addLogsActivity(request, "Block", "Block unsuccessful - User not found")
            return error_response(
                "User not found", "No user exists with the given ID", 404
            )

        if user.userType == "master_admin":
            addLogsActivity(
                request, "Block", "Block unsuccessful - Cannot block master admin"
            )
            return error_response(
                "Action not allowed", "Master admin cannot be blocked", 403
            )

        if user.is_blocked:
            addLogsActivity(
                request, "Block", "Block unsuccessful - User already blocked"
            )
            return error_response("Action not allowed", "User is already blocked", 409)

        # Update user status and block flag
        user.status = data.get("status", False)
        user.is_blocked = data.get("is_blocked", True)

        db.session.commit()

        addLogsActivity(request, "Block", "User blocked successfully")
        return success_response({}, "User blocked successfully", 200)

    except Exception as e:
        db.session.rollback()
        addLogsActivity(request, "Block", "Block unsuccessful - Internal server error")
        return error_response("Failed to block user", str(e), 500)
