import jwt
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify
import os
from dotenv import load_dotenv
from app.models.user import User, db
from functools import wraps

load_dotenv()
SECRET_KEY =os.getenv('JWT_SECRET_KEY')

def generateJWTToken(userId, email):
    # Ensure that secret_key is a string
    if not isinstance(SECRET_KEY, str):
        raise ValueError("secret_key must be a string")
    
    payload = {
        'user_id': userId,
        'email': email,
        'exp': datetime.utcnow() + timedelta(hours=24),  # Token expires in 24 hours
        'iat': datetime.utcnow()  # Token issued at the current time
    }
    
    # Generate JWT token with HS256 algorithm
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

    return token

def verifyJWTToken(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            try:
                # Decode the token (don't use the full auth_header, just the token part)
                decodeToken = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
                # Fetch the user based on the user_id from the token
                user = User.query.filter_by(id=decodeToken.get('user_id')).first()
                if user:
                    request.user = user
                    return func(*args, **kwargs)  # Proceed to the original function
                else:
                    print("User not found in the database.")
                    return jsonify({"error": "User not found"}), 404
            except jwt.ExpiredSignatureError:
                print("Token has expired.")
                return jsonify({"error": "Token has expired"}), 401
            except jwt.InvalidTokenError:
                print("Invalid token.")
                return jsonify({"error": "Invalid token"}), 401
        else:
            print("Authorization header is missing or invalid.")
            return jsonify({"error": "Authorization header is missing or invalid"}), 400

    return decorated_function