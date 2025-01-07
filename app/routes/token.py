import jwt
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify
import os
from dotenv import load_dotenv
from app.models.user import User, db
from functools import wraps

load_dotenv()
SECRET_KEY =os.getenv('JWT_SECRET_KEY')

def generateJWTToken(userId, email,userType):
    if not isinstance(SECRET_KEY, str):
        raise ValueError("secret_key must be a string")  
    payload = {
        'user_id': userId,
        'email': email,
        'userType':userType,
        'exp': datetime.utcnow() + timedelta(hours=24),  # Token expires in 24 hours
        'iat': datetime.utcnow()  # Token issued at the current time
    }
    # Generate JWT token with HS256 algorithm
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

    return token

def verifyJWTToken(allowed_user_types):  # Accept a list of allowed user types
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Get the token from the request headers
            token = request.headers.get('Authorization')

            if not token:
                return jsonify({'error': 'Token is missing'}), 403

            try:
                # Remove the "Bearer " prefix if it's included
                token = token.replace('Bearer ', '')

                # Decode the JWT token using the secret key
                decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
                
                

                # Check if the userType in the token is in the allowed user types list
                if decoded_token['userType'] not in allowed_user_types:
                    return jsonify({'error': f'Access forbidden: This API is only accessible by {", ".join(allowed_user_types)}'}), 403

                checkUser = User.query.filter_by(id=decoded_token['user_id']).first()
                if not checkUser:
                    return jsonify({'error': 'User not found'}), 404
                
                if checkUser.is_blocked==True:
                    return jsonify({"error": "You have been blocked"}), 401
                
                # Add user details to request object for use in the route handler
                request.user = checkUser
                
            except jwt.ExpiredSignatureError:
                return jsonify({'error': 'Token has expired'}), 401
            except jwt.InvalidTokenError:
                return jsonify({'error': 'Invalid token'}), 401

            # Proceed with the original function if token is valid and userType is allowed
            return func(*args, **kwargs)

        return wrapper
    return decorator