from flask import Blueprint, jsonify
from app.models.role import Role, db

# Create a blueprint for roles
roles_bp = Blueprint('roles_routes', __name__)

@roles_bp.route('/list', methods=['GET'])
def get_roles_with_permissions():
    try:
        # Query all roles from the database
        roles = Role.query.all()

        # Serialize roles and their associated permissions
        roles_list = [
            {
                'id': role.id,
                'name': role.name,
                'description': role.description,
                'permissions': [
                    {
                        'id': permission.id,
                        'name': permission.name,
                        'slug': permission.slug,
                        'group': permission.permission_group,
                        'description': permission.description
                    } 
                    for permission in role.permissions  # Assuming many-to-many relationship
                ],
                'created_at': role.created_at,
                'updated_at': role.updated_at
            } 
            for role in roles
        ]
        
        # Return the response as JSON
        return jsonify({
            'success': True,
            'data': roles_list
        }), 200
    except Exception as e:
        # Handle any errors
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
