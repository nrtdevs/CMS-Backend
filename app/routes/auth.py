from flask import Flask,request,jsonify
import re
from cerberus import Validator
from app.models.user import User, db
from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
from .token import generateJWTToken
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
    data = request.get_json()

    if not validator.validate(data):
        return jsonify({"errors": validator.errors}), 400
    
    email = data.get('email')
    password = data.get('password')
    user = User.query.filter_by(email=email).first()
    if user.is_blocked==True:
        return jsonify({"error": "You have been blocked"}), 401
    
    if not user or not check_password_hash(user.password, password):
        return jsonify({"error": "Invalid email or password"}), 401
    
    generatedToken=generateJWTToken(user.id,user.email,user.userType)
  
    return jsonify({
        "message": "Login successful",
        "accessToken":generatedToken,
        "user": {
            "id": user.id,
            "firstName": user.firstName,
            "lastName": user.lastName,
            "email": user.email,
            "role": user.role,
            "mobileNo": user.mobileNo,
        }
    }), 200





