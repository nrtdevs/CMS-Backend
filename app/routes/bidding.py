from flask import Blueprint, request, jsonify
from app.models.bidding import Bidding, db
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import IntegrityError
from cerberus import Validator
from datetime import datetime
from .token import verifyJWTToken
from app.models.user import User, db


biddings_bp = Blueprint('bidding_routes', __name__)

# Validation schema for Bidding
biddingSchema = {
    'userId': {'type': 'integer', 'required': True},
    'projectName': {'type': 'string', 'minlength': 2, 'maxlength': 80, 'required': True},
    'projectDescription': {'type': 'string', 'maxlength': 300, 'required': False},
    'skills': {
        'type': 'list',
        'schema': {'type': 'string', 'minlength': 1, 'maxlength': 80},
        'required': True
    },
    'currency': {'type': 'string', 'maxlength': 80, 'required': False},
    'bidAmount': {'type': 'integer', 'required': False},
    'platform': {'type': 'string', 'minlength': 2, 'maxlength': 80, 'required': True},
    'bidDate': {'type': 'string', 'required': True},
    'clientName': {'type': 'string', 'minlength': 2, 'maxlength': 80, 'required': True},
    'clientEmail': {'type': 'string', 'regex': r'^[^@]+@[^@]+\.[^@]+$', 'required': True},
    'clientContact': {'type': 'integer', 'required': True},
    'clientCompany': {'type': 'string', 'maxlength': 120, 'required': False},
    'clientLocation': {'type': 'string', 'maxlength': 120, 'required': False},
  
}

validator = Validator(biddingSchema)


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
    
    user

    try:
        new_bidding = Bidding(**data)
        db.session.add(new_bidding)
        db.session.commit()
        return jsonify({"message": "Bidding created successfully", "data": new_bidding}), 200
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
        "skills": bidding.skills,
        "currency": bidding.currency,
        "bidAmount": bidding.bidAmount,
        "platform": bidding.platform,
        "bidDate": bidding.bidDate,
        "uploadUrl": bidding.uploadUrl,
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

    paginated_biddings = (
        db.session.query(Bidding)
        .options(
            joinedload(Bidding.user),  # Eager load the associated User
            joinedload(Bidding.project)  # Eager load the associated Project
        )
        .paginate(page=page, per_page=per_page, error_out=False)
    )

    biddings_list = [
        {
            "bidId": bidding.bidId,
            "projectName": bidding.projectName,
            "projectDescription": bidding.projectDescription,
            "skills": bidding.skills,
            "currency": bidding.currency,
            "bidAmount": bidding.bidAmount,
            "platform": bidding.platform,
            "bidDate": bidding.bidDate,
            "uploadUrl": bidding.uploadUrl,
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
                "role": bidding.user.role,
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
            "skills": bidding.skills,
            "currency": bidding.currency,
            "bidAmount": bidding.bidAmount,
            "platform": bidding.platform,
            "bidDate": bidding.bidDate,
            "uploadUrl": bidding.uploadUrl,
            "status": bidding.status,
            "clientName": bidding.clientName,
            "clientEmail": bidding.clientEmail,
            "clientContact": bidding.clientContact,
            "clientCompany": bidding.clientCompany,
            "clientLocation": bidding.clientLocation,
            "remarks": bidding.remarks,
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


