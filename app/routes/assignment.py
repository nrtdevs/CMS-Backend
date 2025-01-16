from flask import Blueprint, request, jsonify
from app.models.assignment import Assignment, db
from app.models.project import Project
from app.models import User
from cerberus import Validator
from .logs import addLogsActivity
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from .token import verifyJWTToken

# Create a Blueprint
assig_bp = Blueprint('assig_routes', __name__)

# Exception handler
def handle_exception(e):
    return jsonify({"message": "An error occurred", "error": str(e)}), 500

assignmentSchema = {
    'title': {'type': 'string', 'minlength': 2, 'maxlength': 100,'required': True,},
    'desc': {'type': 'string','minlength': 5,'maxlength': 500,'required': True,},
    # 'status': {'type': 'string','allowed': ['Pending', 'In Progress', 'Completed', 'On Hold'],},
    # 'priority': {'type': 'string','allowed': ['Low', 'Medium', 'High', 'Critical'],'required': True,},
    'due_date': {'type': 'string','regex': r'^\d{4}-\d{2}-\d{2}$','required': True,},  # Format: YYYY-MM-DD
    'projectId': {'type': 'integer','required': True,},
    'developerId': {'type': 'integer','required': True,},
    'testerId': {'type': 'integer','required': True,},
    'assignedById': {'type': 'integer','required': True,}
}

validator = Validator(assignmentSchema)

# Fetch all assignments
@assig_bp.route('/listByProjectId/<int:projectId>', methods=['GET'])
def get_assignment_list(projectId):
    try:
        # Fetch project data
        project_data = Project.query.filter_by(projectId=projectId).first()
        

        if not project_data:
            return jsonify({'error': 'Project not found'}), 404

        # Include detailed project information
        project_details = {
            "projectId": project_data.projectId,
            "projectName": project_data.bidding.projectName if project_data.bidding else None,
            "status": project_data.status,
        }

        # Serialize assignments with related details
        assignments_data = []
        for assignment in project_data.assignments_list:
            assignments_data.append({
                "id": assignment.id,
                "title": assignment.title,
                "desc": assignment.desc,
                "status": assignment.status,
                "priority": assignment.priority,
                "due_date": assignment.due_date.strftime('%Y-%m-%d') if assignment.due_date else None,
                "created_at": assignment.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                "updated_at": assignment.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
                
                # Including related details
                "project_details": {
                    "projectId": assignment.project.projectId,
                    "name": assignment.project.projectName if assignment.project else None,
                    "status": assignment.project.status if assignment.project else None,
                } if assignment.project else None,
                "developer_details": {
                    "id": assignment.developer.id,
                    "name": f"{assignment.developer.firstName} {assignment.developer.lastName}",
                    "email": assignment.developer.email,
                } if assignment.developer else None,
                "assigner_details": {
                    "id": assignment.assigner.id,
                    "name": f"{assignment.assigner.firstName} {assignment.assigner.lastName}",
                    "email": assignment.assigner.email,
                } if assignment.assigner else None
            })

        return jsonify({
            "success": True,
            "projectDetails": project_details,
            "assignments": assignments_data
        }), 200

    except Exception as e:
        return jsonify({"success": False, "error": f"Internal server error: {str(e)}"}), 500

# Create a new assignment
@assig_bp.route('/create', methods=['POST'])
@verifyJWTToken(['master_admin','user'])
def create_assignment():
    data = request.json
    if not validator.validate(data):
        addLogsActivity(request,'Assigment','Assigment unsuccessfully')
        return jsonify({"errors": validator.errors}), 400
 
    try:
        new_assignment = Assignment(
            projectId=data['projectId'],
            developerId=data['developerId'],
            testerId=data.get('testerId'),
            assignedById=data['assignedById'],
            title=data['title'],
            desc=data['desc'],
            # status=data.get('status', 'Pending'),
            # priority=data.get('priority', 'Medium'),
            due_date=datetime.strptime(data['due_date'], '%Y-%m-%d') if 'due_date' in data else None
        )
        db.session.add(new_assignment)
        db.session.commit()
        addLogsActivity(request,'Register','registration successfully')
        
        return jsonify({"message": "Assignment created successfully", "id": new_assignment.id}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return handle_exception(e)
    except Exception as e:
        return handle_exception(e)

@assig_bp.route('/<int:id>', methods=['GET'])
def get_assignment(id):
    try:
        # Fetch a single assignment by ID
        assignment = Assignment.query.get(id)
        
        if not assignment:
            return jsonify({"message": "Assignment not found"}), 404
        
        # Serialize the assignment with related details
        result = {
            "id": assignment.id,
            "title": assignment.title,
            "desc": assignment.desc,
            "status": assignment.status,
            "priority": assignment.priority,
            "due_date": assignment.due_date.strftime('%Y-%m-%d') if assignment.due_date else None,
            "created_at": assignment.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            "updated_at": assignment.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            
            # Including related details
            "project_details": {
                "id": assignment.project.projectId,
                "name": assignment.project.bidding.projectName,  # Add more fields as necessary
                "status": assignment.project.status,
            } if assignment.project else None,
            "developer_details": {
                "id": assignment.developer.id,
                "name": f"{assignment.developer.firstName} {assignment.developer.lastName}",
                "email": assignment.developer.email,
            } if assignment.developer else None,
            "assigner_details": {
                "id": assignment.assigner.id,
                "name": f"{assignment.assigner.firstName} {assignment.assigner.lastName}",
                "email": assignment.assigner.email,
            } if assignment.assigner else None
        }
        
        return jsonify({"success": True, "data": result}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# Update an assignment
@assig_bp.route('/<int:id>', methods=['PUT'])
def update_assignment(id):
    data = request.json
    try:
        assignment = Assignment.query.get(id)
        if not assignment:
            return jsonify({"message": "Assignment not found"}), 404
        
         # Validate developerId
        if data.get('developerId'):
            developer = User.query.get(data['developerId'])
            if not developer:
                return jsonify({"error": "Invalid developerId"}), 400

        # Validate testerId
        if data.get('testerId'):
            tester = User.query.get(data['testerId'])
            if not tester:
                return jsonify({"error": "Invalid testerId"}), 400


        assignment.projectId = data.get('projectId', assignment.projectId)
        assignment.developerId = data.get('developerId', assignment.developerId)
        assignment.testerId = data.get('testerId', assignment.testerId)
        assignment.assignedById = data.get('assignedById', assignment.assignedById)
        assignment.title = data.get('title', assignment.title)
        assignment.desc = data.get('desc', assignment.desc)
        # assignment.status = data.get('status', assignment.status)
        # assignment.priority = data.get('priority', assignment.priority)
        if 'due_date' in data:
            assignment.due_date = datetime.strptime(data['due_date'], '%Y-%m-%d')
        assignment.updated_at = datetime.utcnow()

        db.session.commit()
        return jsonify({"message": "Assignment updated successfully"}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return handle_exception(e)
    except Exception as e:
        return handle_exception(e)

# Delete an assignment
@assig_bp.route('/<int:id>', methods=['DELETE'])
def delete_assignment(id):
    try:
        assignment = Assignment.query.get(id)
        if not assignment:
            return jsonify({"message": "Assignment not found"}), 404

        db.session.delete(assignment)
        db.session.commit()
        return jsonify({"message": "Assignment deleted successfully"}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return handle_exception(e)
    except Exception as e:
        return handle_exception(e)
