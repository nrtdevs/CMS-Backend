from flask import Flask,request,jsonify
import re
from cerberus import Validator
from app.models.user import User, db
from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
from .token import generateJWTToken
from .notification import create_notification
from .logs import addLogsActivity
from ..helper.response import success_response,error_response

app = Flask(__name__)
secret_key = app.config['SECRET_KEY']

auth_bp = Blueprint('auth_routes', __name__)
loginSchema = {
    'email': {'type': 'string', 'regex': r'^[^@]+@[^@]+\.[^@]+$', 'required': True},
    'password': {'type': 'string', 'minlength': 8, 'maxlength': 50, 'required': True},
  }

validator = Validator(loginSchema)


@auth_bp.route ('/login',methods=['POST'])
def login():
    try:
        data = request.get_json()
    
        if not validator.validate(data):
            raise ValueError({"validation_errors": validator.errors})
        
        email = data.get('email')
        password = data.get('password')
        user = User.query.filter_by(email=email).first()
        request.user=user
        
        if  not user:
            raise ValueError({"error": "User not found"})
        if user.is_blocked==True:
            raise ValueError({"error": "You have been blocked"})
        
        if not check_password_hash(user.password, password):
            raise ValueError({"error": "Invalid email or password"})
    
        generatedToken=generateJWTToken(user.id,user.email,user.userType)
        
        new_notification = {
            "user_id": user.id,
            "message": "User logged in",
            "module": "auth",
            "subject":"Login"
        }
        
        create_notification(new_notification)
        
        
        addLogsActivity(request,'Login','login successfully')
        
        role_data = {
            "id": user.role.id,
            "name": user.role.name,
            "permissions": [
                {"id": perm.id, "slug": perm.slug} for perm in user.role.permissions
            ] if user.role.permissions else None
        } if user.role else None
        
        
        data = {
            "accessToken": generatedToken,
            "user": {
                "id": user.id,
                "firstName": user.firstName,
                "lastName": user.lastName,
                "email": user.email,
                "roleDetails": role_data,
                "mobileNo": user.mobileNo,
            }
        }
        return success_response(data,"Login successful", 200)
    except ValueError as e:
        
        return error_response("Login failed", e.args[0], 401)
    except Exception as e:
        return error_response("An unexpected error occurred during login", str(e), 500)




