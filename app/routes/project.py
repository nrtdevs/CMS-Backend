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
EditProjectSchema = {
    'projectId': {'type': 'integer', 'required': True},    
    'teachLead': {
        'type': 'list',
        'schema': {'type': 'string', 'minlength': 1, 'maxlength': 80},
        'required': False
    },
    'frontDev': {
        'type': 'list',
        'schema': {'type': 'string', 'minlength': 1, 'maxlength': 80},
        'required': False
    },
    'backDev': {
        'type': 'list',
        'schema': {'type': 'string', 'minlength': 1, 'maxlength': 80},
        'required': False
    },
    'tester': {
        'type': 'list',
        'schema': {'type': 'string', 'minlength': 1, 'maxlength': 80},
        'required': False
    },
    'currency': {'type': 'string', 'maxlength': 80, 'required': False},
    'totalBudget': {'type': 'integer', 'required': False},
    'startDate': {'type': 'string', 'required': False},
    'deadlineDate': {'type': 'string', 'required': False},
    'approvedBy': {'type': 'integer', 'required': False},
}
Edit_validator = Validator(EditProjectSchema)

@projects_bp.route('/project/<int:projectId>', methods=['PUT'])
@verifyJWTToken(['master_admin'])
def update_bidding(projectId):
    data = request.get_json()
    if not Edit_validator.validate(data):
        return jsonify({"errors": Edit_validator.errors}), 400
    
    project= Project.query.filter_by(projectId=projectId).first()

    if not project:
        return jsonify({'error': 'Project not found'}), 404

    # Update fields
    for key, value in data.items():
        if hasattr(project, key):
            setattr(project, key, value)
    db.session.commit()

    return jsonify({"message": "Project updated successfully"}), 200
