import jwt
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify
import os
from dotenv import load_dotenv
from app.models.user import User, db
from app.models import Token
from functools import wraps

load_dotenv()
SECRET_KEY = os.getenv('JWT_SECRET_KEY')

def generateJWTToken(userId, email, userType):
    if not isinstance(SECRET_KEY, str):
        raise ValueError("SECRET_KEY must be a string")

    # Check if a valid token already exists for the user
    existing_token = Token.query.filter_by(userId=userId).first()
    if existing_token and existing_token.expiryAt > datetime.utcnow(): 
        return existing_token.accessToken

    # If no valid token exists, create a new one
    expiry_time = datetime.utcnow() + timedelta(hours=24)
    new_token = Token(
        userId=userId,
        expiryAt=expiry_time
    )
    db.session.add(new_token)
    db.session.commit()

    # Generate JWT token with the new token ID
    payload = {
        'jwtId': new_token.tokenId,
        'user_id': userId,
        'email': email,
        'userType': userType,
        'exp': expiry_time,  # Token expires in 24 hours
        'iat': datetime.utcnow()  # Token issued at the current time
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    new_token.accessToken=token
    db.session.commit()
    return token


def verifyJWTToken(allowed_user_types):
    """Decorator to verify JWT tokens and ensure user authorization."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Get the token from the request headers
            token = request.headers.get('Authorization')
            if not token:
                return jsonify({'error': 'Token is missing'}), 403

            try:
                # Remove the "Bearer " prefix if present
                token = token.replace('Bearer ', '')

                # Decode the JWT token using the secret key
                decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])

                # Check if the userType in the token is allowed
                if decoded_token['userType'] not in allowed_user_types:
                    return jsonify({'error': f'Access forbidden: This API is only accessible by {", ".join(allowed_user_types)}'}), 403

                # Verify the token exists in the database and is associated with the correct user
                stored_token = Token.query.filter_by(tokenId=decoded_token['jwtId']).first()
                if not stored_token or stored_token.expiryAt < datetime.utcnow():
                    return jsonify({'error': 'Invalid or expired token'}), 403

                # Ensure the token belongs to the correct user
                user = User.query.filter_by(id=stored_token.userId).first()
                if not user:
                    return jsonify({'error': 'User not found'}), 404

                request.user = user  # Attach the user to the request

            except jwt.ExpiredSignatureError:
                return jsonify({'error': 'Token has expired'}), 401
            except jwt.InvalidTokenError:
                return jsonify({'error': 'Invalid token'}), 401

            # Proceed with the original function
            return func(*args, **kwargs)
        return wrapper
    return decorator


def check_permissions(required_permissions):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user = getattr(request, 'user', None)  # Get the user object from the request
            if not user:
                return jsonify({'error': 'User not authenticated'}), 401
            
            # Ensure role and permissions are accessible
            role = getattr(user, 'role', None)
            if not role or not hasattr(role, 'permissions'):
                return jsonify({'error': 'User role or permissions not found'}), 403

            # print("User Permissions:", role.permissions)  # Debugging output

            # Extract slugs from Permission objects
            user_permissions = [perm.slug for perm in role.permissions]

            # Check if the user has any of the required permissions
            if any(perm in user_permissions for perm in required_permissions):
                return func(*args, **kwargs)

            # If no permissions match, deny access
            return jsonify({'error': 'Access forbidden: Missing required permissions'}), 403
        return wrapper
    return decorator
