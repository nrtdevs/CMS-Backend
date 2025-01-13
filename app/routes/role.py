from flask import Blueprint, jsonify,request
from app.models.role import Role, db
from cerberus import Validator
from app.models.permission import Permission  # Assuming there's a Permission model
from slugify import slugify
from .token import verifyJWTToken

# Create a blueprint for roles
roles_bp = Blueprint('roles_routes', __name__)

# CreateRoleSchema with Cerberus validation
CreateRoleSchema = {
    'name': {'type': 'string', 'minlength': 1, 'maxlength': 100, 'required': True},
    'userType': { 
        'type': 'string', 
        'allowed': ['user', 'superadmin'],
        'required': True
    },
    'description': {'type': 'string', 'minlength': 1, 'maxlength': 200, 'required': False},
    'permissions': {
        'type': 'list',
        'schema': {'type': 'integer', 'min': 1},
        'required': False
    }
}
UpdateRoleSchema = {
    'name': {'type': 'string', 'minlength': 1, 'maxlength': 100, 'required': True},
  
    'description': {'type': 'string', 'minlength': 1, 'maxlength': 200, 'required': False},
    'permissions': {
        'type': 'list',
        'schema': {'type': 'integer', 'min': 1},
        'required': False
    }
}

validator = Validator(CreateRoleSchema)

# Create Roles
@roles_bp.route('/create', methods=['POST'])
@verifyJWTToken(['master_admin', 'super_admin'])
def create_role():
    data = request.get_json()
    if not validator.validate(data):
        return jsonify({'errors': validator.errors}), 400

    # Extract data
    name = data['name']
    userType = data['userType']
    description = data.get('description')
    permissions = data.get('permissions', [])
    
    # Check if the role already exists
    existing_role = Role.query.filter_by(name=name).first()
    if existing_role:
          return jsonify({'message': f"Role '{name}' already exists."}), 400  # Prevent duplicate role creation

    # List to hold valid permissions
    all_permissions = []  # Corrected variable name

    # Loop through provided permissions and validate them
    for perm_id in permissions:
        permission = Permission.query.get(perm_id)
        if permission:
            all_permissions.append(permission)
        else:
            return jsonify({'message': f"Invalid permission ID: {perm_id}"}), 400 
            
    
    # Create the role object
    role = Role(name=name, userType=userType, description=description)
    
    # Associate the valid permissions with the role
    role.permissions.extend(all_permissions)

    # Create and save the role to the database
    db.session.add(role)
    db.session.commit()

    # Return a success message with role details
    return jsonify({'message': 'Role created successfully!', 'role': {'id': role.id, 'name': role.name, 'userType': role.userType}}), 201

@roles_bp.route('/list', methods=['GET'])
@verifyJWTToken(['master_admin', 'super_admin','user'])
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
#get a single role by its id and its associated permission
@roles_bp.route('/<int:role_id>', methods=['GET'])
@verifyJWTToken(['master_admin', 'super_admin','user'])
def get_role_by_id(role_id):
    try:
        # Validate the role_id to ensure it's an integer (Flask's URL converters handle this)
        if not isinstance(role_id, int):
            return jsonify({
                'success': False,
                'message': 'Invalid role_id format'
            }), 400
        
        # Query role by id
        role = Role.query.get(role_id)
        
        if not role:
            return jsonify({
                'success': False,
                'message': 'Role not found'
            }), 404
        
        # Serialize the role and its associated permissions
        role_data = {
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
                for permission in role.permissions  # Many-to-many relationship
            ],
            'created_at': role.created_at,
            'updated_at': role.updated_at
        }
        
        return jsonify({
            'success': True,
            'data': role_data
        }), 200
    except Exception as e:
        # Handle any errors
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@roles_bp.route('/update/<int:role_id>', methods=['PUT'])
@verifyJWTToken(['master_admin', 'super_admin','user'])
def update_role(role_id):
    data = request.get_json()

    # Validate and extract new data
    validator = Validator(UpdateRoleSchema)
    if not validator.validate(data):
        return jsonify({'errors': validator.errors}), 400

    # Find the role to update
    role = Role.query.get(role_id)
    if not role:
        return jsonify({"message": "Role not found."}), 404

    # Update role data
    role.name = data['name']
    role.description = data.get('description', role.description)

    # Get provided permissions from the request
    permissions = data.get('permissions', [])
    
    # List to hold valid permissions
    all_permissions = []  

    # Loop through provided permissions and validate them
    for perm_id in permissions:
        permission = Permission.query.get(perm_id)
        if permission:
            all_permissions.append(permission)  # Append valid permission to the list
        else:
            return jsonify({'message': f"Invalid permission ID: {perm_id}"}), 400  # Return an error for invalid permission IDs
    
    # Update the permissions for the role
    role.permissions = all_permissions  # Update the permissions list

    # Commit changes to the database
    db.session.commit()

    # Return a success message with role details
    return jsonify({'message': 'Role updated successfully!', 'role': {'id': role.id, 'name': role.name, 'description': role.description}}), 200
        
    
