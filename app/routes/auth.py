from flask import Flask,request,jsonify
from cerberus import Validator
from app.models.user import User
from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
from .token import generateJWTToken
from .logs import createActivityLogs
from user_agents import parse

auth_bp = Blueprint("auth_routes", __name__)


app = Flask(__name__)
secret_key = app.config['SECRET_KEY']

auth_bp = Blueprint('auth_routes', __name__)
loginSchema = {
    'email': {'type': 'string', 'regex': r'^[^@]+@[^@]+\.[^@]+$', 'required': True},
    'password': {'type': 'string', 'minlength': 8, 'maxlength': 50, 'required': True},
  }

validator = Validator(loginSchema)

# Helper function to extract user-agent details
def extract_user_agent_details():
    user_agent_string = request.headers.get("User-Agent", "Unknown")
    user_agent = parse(user_agent_string)

    return {
        "browser": f"{user_agent.browser.family} {user_agent.browser.version_string}",
        "os": f"{user_agent.os.family} {user_agent.os.version_string}",
        "device": user_agent.device.family,
        "is_mobile": user_agent.is_mobile,
        "is_tablet": user_agent.is_tablet,
        "is_pc": user_agent.is_pc,
    }

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
    
    # Extract IP address and user-agent details
    
    ip_address = request.remote_addr or "Unknown"
    user_agent_details = extract_user_agent_details()
  
    # Prepare log data
    logData = {
        "activity": "login",
        "desc": "Successful login",
        "userId": user.id,
        "ipAddress": ip_address,
        "userAgent": user_agent_details["browser"],
        "device": user_agent_details["device"],
    }
    createActivityLogs(logData)

  
    # Return the response with serialized log data
    return jsonify({
        "message": "Login successful",
        "accessToken": generatedToken,
        "user": {
            "id": user.id,
            "firstName": user.firstName,
            "lastName": user.lastName,
            "email": user.email,
            "role": user.role,
            "mobileNo": user.mobileNo,
        }
    }), 200




