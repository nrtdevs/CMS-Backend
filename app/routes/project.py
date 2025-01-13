from flask import Blueprint, request, jsonify
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import IntegrityError
from cerberus import Validator
from datetime import datetime
from .token import verifyJWTToken
from app.models.user import User, db
from app.models.project import Project, db

projects_bp = Blueprint('project_routes', __name__)
EditProjectSchema = {
    'projectId': {'type': 'integer', 'required': True},    
    'teachLead': {
        'type': 'list',
        'schema': {'type': 'string', 'minlength': 1, 'maxlength': 80},
        'required': False
    },'developer_id': {
        'type': 'list',
        'schema': {'type': 'integer'},
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


# READ single project
@projects_bp.route('/<int:projectId>', methods=['GET'])
@verifyJWTToken(['master_admin', 'user'])
def get_project(projectId):
    project = (
        db.session.query(Project)
        .filter_by(projectId=projectId)
        .first()
    )
    if not project:
        return jsonify({'error': 'Project not found'}), 404
        # Serialize the user and project relationships
    # user_data = {
    #     "id": project.user.id,
    #     "firstName": project.user.firstName,
    #     "lastName": project.user.lastName,
    #     "role": project.user.role,
    # } if project.user else None

      # Serialize assignments
    assignments_data = [
        {
            "assignmentId": assignment.id,
            "title": assignment.title,
            "desc": assignment.desc,
            "status": assignment.status,

            "created_at": assignment.created_at,
            "updated_at": assignment.updated_at,
        }
        for assignment in project.assignments_list
    ]
    project_data = {
        "projectId": project.projectId,
        "frontDev": project.frontDev,
        "backDev": project.frontDev,
        "teachLead": project.teachLead,
        "tester": project.tester,
        "status": project.status,
        "currency": project.currency,
        "totalBudget": project.totalBudget,
        "startDate": project.startDate,
        "deadlineDate": project.deadlineDate,
        "approvedBy": project.approvedBy,
        "created_at" : project.created_at,
        "assignments_list":assignments_data
    }

    return jsonify({"message": "Project fetched successfully", "data": project_data}), 200



# @projects_bp.route('/project/<int:projectId>', methods=['PUT'])
# @verifyJWTToken(['master_admin'])
# def update_project(projectId):
#     data = request.get_json()
#     if not Edit_validator.validate(data):
#         return jsonify({"errors": Edit_validator.errors}), 400
    
#     project= Project.query.filter_by(projectId=projectId).first()

#     if not project:
#         return jsonify({'error': 'Project not found'}), 404

#     # Update fields
#     for key, value in data.items():
#         if hasattr(project, key):
#             setattr(project, key, value)
#     db.session.commit()

#     return jsonify({"message": "Project updated successfully"}), 200
