from flask import Blueprint, request, jsonify
from app.models.bidding import Bidding, db
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import IntegrityError
from cerberus import Validator
from datetime import datetime
from .token import verifyJWTToken
from app.models.user import User, db
from app.models.project import Project, db

projects_bp = Blueprint('bidding_routes', __name__)
approvedSchema = {
    'bidId': {'type': 'integer', 'required': True},    
    'teachLead': {
        'type': 'list',
        'schema': {'type': 'string', 'minlength': 1, 'maxlength': 80},
        'required': True
    },
    'frontDev': {
        'type': 'list',
        'schema': {'type': 'string', 'minlength': 1, 'maxlength': 80},
        'required': True
    },
    'backDev': {
        'type': 'list',
        'schema': {'type': 'string', 'minlength': 1, 'maxlength': 80},
        'required': True
    },
    'tester': {
        'type': 'list',
        'schema': {'type': 'string', 'minlength': 1, 'maxlength': 80},
        'required': True
    },
    'currency': {'type': 'string', 'maxlength': 80, 'required': False},
    'totalBudget': {'type': 'integer', 'required': False},
    'startDate': {'type': 'string', 'required': True},
    'deadlineDate': {'type': 'string', 'required': True},
    'approvedBy': {'type': 'integer', 'required': True},
}
approve_validator = Validator(approvedSchema)

@projects_bp.route('/project/<int:bidId>', methods=['PUT'])
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
