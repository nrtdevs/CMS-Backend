from flask import Blueprint, request, jsonify
from app.models.bidding import Bidding, db
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import IntegrityError
from cerberus import Validator
from datetime import datetime
from .token import verifyJWTToken
from app.models.user import User, db
from app.models.project import Project, db
from app.models.role import Role
from app.models.team import Team
from .file_uploader import handle_file_upload
import os


biddings_bp = Blueprint('bidding_routes', __name__)

# Validation schema for Bidding
biddingSchema = {
    'userId': {'type': 'integer', 'required': True},
    'projectName': {'type': 'string', 'minlength': 2, 'maxlength': 80, 'required': True},
    'projectDescription': {'type': 'string', 'maxlength': 300, 'required': False},
    'currency': {'type': 'string', 'maxlength': 80, 'required': False},
    'bidAmount': {'type': 'integer', 'required': False},
    'platform': {'type': 'string', 'minlength': 2, 'maxlength': 80, 'required': True},
    'bidDate': {'type': 'string', 'required': True},
    'clientName': {'type': 'string', 'minlength': 2, 'maxlength': 80, 'required': True},
    'clientEmail': {'type': 'string', 'regex': r'^[^@]+@[^@]+\.[^@]+$', 'required': True},
    'clientContact': {'type': 'integer', 'required': True},
    'clientCompany': {'type': 'string', 'maxlength': 120, 'required': False},
    'countryCode': {'type': 'string', 'maxlength': 120, 'required': False},
    'clientLocation': {'type': 'string', 'maxlength': 120, 'required': False},
    'remarks': {'type': 'string', 'maxlength': 500, 'required': False}, 
    'commission': {'type': 'boolean', 'required': True}, 


}

approvedSchema = {
    'bidId': {'type': 'integer', 'required': True},    
    'techLeadId': {'type': 'integer', 'required': True},
    'developerIds': {
        'type': 'list',
        'schema': {'type': 'integer'},
        'required': False
    },
    "teamId":{'type': 'integer', 'required': False},
    'currency': {'type': 'string', 'maxlength': 80, 'required': False},
    'totalBudget': {'type': 'integer', 'required': False},
    'startDate': {'type': 'string', 'required': True},
    'deadlineDate': {'type': 'string', 'required': True},
    'approvedById': {'type': 'integer', 'required': True},
}
def auto_convert(data, schema):
    """
    Automatically converts and validates data based on the provided schema.
    
    Args:
        data (dict): The input data to be validated and converted.
        schema (dict): The schema defining the expected types and requirements.
    
    Returns:
        dict: Converted and validated data.
    
    Raises:
        ValueError: If a field is invalid or conversion fails.
    """
    converted_data = {}

    for key, field in schema.items():
        if field.get('required') and key not in data:
            raise ValueError(f"'{key}' is required but not provided.")

        if key not in data:
            # Skip if the field is not required and not in the data
            continue

        value = data[key]

        # Convert based on the type defined in the schema
        if field['type'] == 'integer':
            try:
                converted_data[key] = int(value)
            except ValueError:
                raise ValueError(f"'{key}' should be an integer. Received: {value}")

        elif field['type'] == 'string':
            if 'maxlength' in field and len(value) > field['maxlength']:
                raise ValueError(f"'{key}' exceeds the maximum length of {field['maxlength']}.")
            converted_data[key] = str(value)

        elif field['type'] == 'list':
            if not isinstance(value, list):
                # Convert single integers or comma-separated strings into a list
                if isinstance(value, int):
                    value = [value]
                elif isinstance(value, str):
                    value = value.split(',')
                else:
                    raise ValueError(f"'{key}' should be a list. Received: {value}")
            if 'schema' in field and field['schema']['type'] == 'integer':
                try:
                    converted_data[key] = [int(item) for item in value]
                except ValueError:
                    raise ValueError(f"'{key}' should be a list of integers. Received: {value}")
            else:
                converted_data[key] = value

        elif field['type'] == 'date':
            try:
                converted_data[key] = datetime.strptime(value, '%Y-%m-%d').date()
            except ValueError:
                raise ValueError(f"'{key}' should be a date in YYYY-MM-DD format. Received: {value}")

        else:
            raise ValueError(f"Unsupported type '{field['type']}' in schema for '{key}'.")

    return converted_data

validator = Validator(biddingSchema)
approve_validator = Validator(approvedSchema)


# CREATE Bidding
@biddings_bp.route('/create', methods=['POST'])
@verifyJWTToken(['master_admin','user'])
def create_bidding():
    data = request.get_json()
    if not validator.validate(data):
        return jsonify({"errors": validator.errors}), 400
    try:
        data['bidDate'] = datetime.strptime(data['bidDate'], '%Y-%m-%d').date()
    except ValueError:
        return jsonify({"error": "Invalid bidDate format. Use YYYY-MM-DD."}), 400

    
    userId = data.get('userId')
    user = User.query.filter_by(id=userId,status=True).first()
    if not user:
        return jsonify({'error': 'User not found or not active'}), 404

    try:
        bidding = Bidding(**data)
        db.session.add(bidding)
        db.session.commit()
        
        user_data = {
            "id": bidding.user.id,
            "firstName": bidding.user.firstName,
            "lastName": bidding.user.lastName,
            "role": bidding.user.role,
        } if bidding.user else None

        project_data = {
            "projectId": bidding.project.projectId,
            "projectName": bidding.project.projectName,
            "status": bidding.project.status,
        } if bidding.project else None

        bidding_data = {
            "bidId": bidding.bidId,
            "projectName": bidding.projectName,
            "projectDescription": bidding.projectDescription,
            "currency": bidding.currency,
            "bidAmount": bidding.bidAmount,
            "platform": bidding.platform,
            "bidDate": bidding.bidDate,
            "status": bidding.status,
            "clientName": bidding.clientName,
            "clientEmail": bidding.clientEmail,
            "clientContact": bidding.clientContact,
            "clientCompany": bidding.clientCompany,
            "clientLocation": bidding.clientLocation,
            "remarks": bidding.remarks,
            "user_id": user_data,
            "commission": bidding.commission,
            "project_id":project_data,
            # "approvedBy": bidding.approvedBy,
        }
    
        return jsonify({"message": "Bidding created successfully", "data": bidding_data}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An error occurred while creating the bidding.", "details": str(e)}), 500


# READ single Bidding
@biddings_bp.route('/<int:bidId>', methods=['GET'])
@verifyJWTToken(['master_admin', 'user'])
def get_bidding(bidId):
    bidding = (
        db.session.query(Bidding)
        .options(
            joinedload(Bidding.user),  # Eager load the associated User
            joinedload(Bidding.project)  # Eager load the associated Project
        )
        .filter_by(bidId=bidId)
        .first()
    )
    if not bidding:
        return jsonify({'error': 'Bidding not found'}), 404
        # Serialize the user and project relationships
    user_data = {
        "id": bidding.user.id,
        "firstName": bidding.user.firstName,
        "lastName": bidding.user.lastName,
        "role": bidding.user.role.id,
    } if bidding.user else None

    project_data = {
        "projectId": bidding.project.projectId,
        # "tester": bidding.project.tester,
        "status": bidding.project.status,
        "currency": bidding.project.currency,
        "totalBudget": bidding.project.totalBudget,
        "startDate": bidding.project.startDate,
        "deadlineDate": bidding.project.deadlineDate,
        "assignedById": bidding.project.assignedById,
        "created_at" : bidding.project.created_at
   
    } if bidding.project else None

    bidding_data = {
        "bidId": bidding.bidId,
        "projectName": bidding.projectName,
        "projectDescription": bidding.projectDescription,
        "currency": bidding.currency,
        "bidAmount": bidding.bidAmount,
        "platform": bidding.platform,
        "bidDate": bidding.bidDate,
        "status": bidding.status,
        "clientName": bidding.clientName,
        "clientEmail": bidding.clientEmail,
        "clientContact": bidding.clientContact,
        "clientCompany": bidding.clientCompany,
        "clientLocation": bidding.clientLocation,
        "remarks": bidding.remarks,
        "user_id": user_data,
        "project_id":project_data,
    }

    return jsonify({"message": "Bidding fetched successfully", "data": bidding_data}), 200

# READ all Biddings with user and project populate for Master Admin
@biddings_bp.route('/all', methods=['GET'])
@verifyJWTToken(['master_admin'])
def get_biddings():
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)
    search_query = request.args.get('search', default='', type=str)
    status_filter = request.args.get('status', default='', type=str)

    query = db.session.query(Bidding).options(
        joinedload(Bidding.user),
        joinedload(Bidding.project)
    )

    # Apply search filter if present
    if search_query:
        search_filter = f"%{search_query}%"
        query = query.filter(
            (Bidding.projectName.ilike(search_filter)) |
            (Bidding.clientName.ilike(search_filter)) |
            (Bidding.clientEmail.ilike(search_filter)) |
            (Bidding.remarks.ilike(search_filter))
        )

    # Apply status filter if present
    if status_filter:
        query = query.filter(Bidding.status == status_filter)

    paginated_biddings = query.paginate(page=page, per_page=per_page, error_out=False)

    biddings_list = [
        {
            "bidId": bidding.bidId,
            "projectName": bidding.projectName,
            "projectDescription": bidding.projectDescription,
            "currency": bidding.currency,
            "bidAmount": bidding.bidAmount,
            "platform": bidding.platform,
            "bidDate": bidding.bidDate,
            "status": bidding.status,
            "clientName": bidding.clientName,
            "clientEmail": bidding.clientEmail,
            "clientContact": bidding.clientContact,
            "clientCompany": bidding.clientCompany,
            "clientLocation": bidding.clientLocation,
            "remarks": bidding.remarks,
            "user": {
                "id": bidding.user.id,
                "firstName": bidding.user.firstName,
                "lastName": bidding.user.lastName,
                "role": str(bidding.user.role),
            } if bidding.user else None,
            "project": {
                "projectId": bidding.project.projectId,
                "projectName": bidding.project.projectName,
                "status": bidding.project.status,
            } if bidding.project else None,
        }
        for bidding in paginated_biddings.items
    ]

    return jsonify({
        "message": "Biddings fetched successfully",
        "data": biddings_list,
        "pagination": {
            "page": paginated_biddings.page,
            "per_page": paginated_biddings.per_page,
            "total_pages": paginated_biddings.pages,
            "total_items": paginated_biddings.total,
        }
    }), 200


# @biddings_bp.route('/all', methods=['GET'])
# @verifyJWTToken(['master_admin'])
# def get_biddings():
#     page = request.args.get('page', default=1, type=int)
#     per_page = request.args.get('per_page', default=10, type=int)

#     paginated_biddings = (
#         db.session.query(Bidding)
#         .options(
#             joinedload(Bidding.user),  # Eager load the associated User
#             joinedload(Bidding.project)  # Eager load the associated Project
#         )
#         .paginate(page=page, per_page=per_page, error_out=False)
#     )

#     biddings_list = [
#         {
#             "bidId": bidding.bidId,
#             "projectName": bidding.projectName,
#             "projectDescription": bidding.projectDescription,
#             "currency": bidding.currency,
#             "bidAmount": bidding.bidAmount,
#             "platform": bidding.platform,
#             "bidDate": bidding.bidDate,
#             "status": bidding.status,
#             "clientName": bidding.clientName,
#             "clientEmail": bidding.clientEmail,
#             "clientContact": bidding.clientContact,
#             "clientCompany": bidding.clientCompany,
#             "clientLocation": bidding.clientLocation,
#             "remarks": bidding.remarks,
#             "user": {
#                 "id": bidding.user.id,
#                 "firstName": bidding.user.firstName,
#                 "lastName": bidding.user.lastName,
#                 "role": str(bidding.user.role),
#             } if bidding.user else None,
#             "project": {
#                 "projectId": bidding.project.projectId,
#                 "projectName": bidding.project.projectName,
#                 "status": bidding.project.status,
#             } if bidding.project else None,
#         }
#         for bidding in paginated_biddings.items
#     ]

#     return jsonify({
#         "message": "Biddings fetched successfully",
#         "data": biddings_list,
#         "pagination": {
#             "page": paginated_biddings.page,
#             "per_page": paginated_biddings.per_page,
#             "total_pages": paginated_biddings.pages,
#             "total_items": paginated_biddings.total,
#         }
#     }), 200


@biddings_bp.route('/list/<int:userId>', methods=['GET'])
@verifyJWTToken(['master_admin', 'user'])
def get_biddings_by_user(userId):
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)
    paginated_biddings = (
        db.session.query(Bidding)
        .options(
            joinedload(Bidding.user),  # Eager load the associated User
            joinedload(Bidding.project)  # Eager load the associated Project
        ).filter(Bidding.userId == userId) 
        .paginate(page=page, per_page=per_page, error_out=False)
    )

    biddings_list = [
        {
            "bidId": bidding.bidId,
            "projectName": bidding.projectName,
            "projectDescription": bidding.projectDescription,
            "currency": bidding.currency,
            "bidAmount": bidding.bidAmount,
            "platform": bidding.platform,
            "bidDate": bidding.bidDate.strftime("%Y-%m-%d") if bidding.bidDate else None,
            "status": bidding.status,
            "clientName": bidding.clientName,
            "clientEmail": bidding.clientEmail,
            "clientContact": bidding.clientContact,
            "clientCompany": bidding.clientCompany,
            "clientLocation": bidding.clientLocation,
            "remarks": bidding.remarks,
            "user": {
                "userId": bidding.user.id if bidding.user else None,
                "firstName": bidding.user.firstName if bidding.user else None,
                "lastName": bidding.user.lastName if bidding.user else None,                
                "userEmail": bidding.user.email if bidding.user else None,
            },
            "project": {
                "projectId": bidding.project.projectId if bidding.project else None,
                "startDate": bidding.project.startDate.strftime("%Y-%m-%d") if bidding.project and bidding.project.startDate else None,
                "deadlineDate": bidding.project.deadlineDate.strftime("%Y-%m-%d") if bidding.project and bidding.project.deadlineDate else None,
                "status": bidding.project.status if bidding.project else None,
                }
            }
        
        for bidding in paginated_biddings.items
    ]

    return jsonify({
        "message": "Biddings fetched successfully",
        "data": biddings_list,
        "pagination": {
            "page": paginated_biddings.page,
            "per_page": paginated_biddings.per_page,
            "total_pages": paginated_biddings.pages,
            "total_items": paginated_biddings.total,
        }
    }), 200

# UPDATE Bidding
@biddings_bp.route('/bidding/<int:bidId>', methods=['PUT'])
@verifyJWTToken(['master_admin'])
def update_bidding(bidId):
    data = request.get_json()
    bidding = Bidding.query.filter_by(bidId=bidId).first()

    if not bidding:
        return jsonify({'error': 'Bidding not found'}), 404

    # Update fields
    for key, value in data.items():
        if hasattr(bidding, key):
            setattr(bidding, key, value)

    db.session.commit()

    return jsonify({"message": "Bidding updated successfully"}), 200

# Approve Bidding
@biddings_bp.route('/approve', methods=['POST'])
@verifyJWTToken(['master_admin','user'])
@handle_file_upload(allowed_extensions={'pdf'}, upload_folder='uploads')

def approve_bidding(file_path, file_name):
    

    data = request.form.to_dict()
    try:
        validated_data = auto_convert(data, approvedSchema)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400



    # Extract validated data
    bidId = validated_data.get('bidId')
    approvedById = validated_data.get('approvedById')
    techLeadId = validated_data.get('techLeadId')
    startDate = validated_data.get('startDate')
    deadlineDate = validated_data.get('deadlineDate')
    currency = validated_data.get('currency')
    totalBudget = validated_data.get('totalBudget')
    developer_ids = validated_data.get('developerIds', [])
    team_id = validated_data.get('teamId')
    developerData = []

    bidding = Bidding.query.filter_by(bidId=bidId).first()
    techLead = User.query.filter_by(id=techLeadId).first()
    approvedBy = User.query.filter_by(id=approvedById).first()
    userData = User.query.filter_by(id=bidding.userId).first()
    
    
    if not bidding:
        return jsonify({'error': 'Bidding not found'}), 404
    if bidding.status == 'approved':
        return jsonify({'error': 'Bidding already approved'}), 400    

    if approvedById != bidding.userId and approvedById != 1:
        return jsonify({'error': 'You are not authorized to approve this bidding'}), 403
    
    if not techLead:
        return jsonify({'error': 'TechLead not found'}), 404
        
    if team_id:
        team = Team.query.filter_by(teamId=team_id).first()
        if not team:
            return jsonify({'error': f"Team with ID {team_id} not found"}), 404
        
        team_developer_ids = [developer.id for developer in team.developers]
        developer_ids = team_developer_ids
 
        
    if developer_ids:
        developers = User.query.filter(User.id.in_(developer_ids)).all()
        if len(developers) != len(developer_ids):
            missing_devs = [dev_id for dev_id in developer_ids if dev_id not in [dev.id for dev in team_developer_ids]]
            return jsonify({'error': f"Some developer IDs are invalid: {missing_devs}"}), 404
        developerData = developers

    try:
        project_data = {
            "projectName":bidding.projectName,
            "currency": currency,
            "totalBudget": totalBudget,
            "techLeadId": techLeadId,
            "assignedById": approvedBy.id,
            "startDate": startDate,
            "deadlineDate": deadlineDate,
            "userId": userData.id,
            "bidId": bidId,
        }

        project = Project(**project_data)
        db.session.add(project)
        db.session.commit()

        # After committing the project, we update the bidding
        if project:
            bidding.projectId = project.projectId
            bidding.status = 'approved'
            bidding.approvedBy = approvedBy.id
            db.session.commit()
        # Add developers to the project
        for developer in developerData:
            project.developers.append(developer)  # Assuming many-to-many relationship 
        db.session.commit()

        return jsonify({"message": "Bidding approved successfully", "file_path": file_path, "file_name": file_name}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An error occurred while approving the bidding.", "details": str(e)}), 500



