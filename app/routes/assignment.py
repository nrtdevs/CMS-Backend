from flask import Blueprint, request, jsonify
from app.models.assignment import Assignment, db
from app.models.project import Project
from app.models import User
from app.models import db, Remark
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
    'status': {'type': 'string','allowed': ['Pending', 'In Progress', 'Completed', 'On Hold'],},
    'priority': {'type': 'string','allowed': ['Low', 'Medium', 'High', 'Critical'],'required': True,},
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
                "tester_details": {
                    "id": assignment.tester.id,
                    "name": f"{assignment.tester.firstName} {assignment.tester.lastName}",
                    "email": assignment.tester.email,
                } if assignment.tester else None,
                "assigner_details": {
                    "id": assignment.assigner.id,
                    "name": f"{assignment.assigner.firstName} {assignment.assigner.lastName}",
                    "email": assignment.assigner.email,
                } if assignment.assigner else None
            })

        return jsonify({
            "success": True,
            # "projectDetails": project_details,
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
            status=data.get('status', 'Pending'),
            priority=data.get('priority', 'Medium'),
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
@verifyJWTToken(['master_admin', 'user'])
def update_assignment(id):
    data = request.json

    # Validate input data against the schema
    if not validator.validate(data):
        return jsonify({"error": "Invalid data", "details": validator.errors}), 400

    try:
        # Fetch the assignment by ID
        assignment = Assignment.query.get(id)
        if not assignment:
            return jsonify({"message": "Assignment not found"}), 404

        # Validate developerId if provided
        if data.get('developerId'):
            developer = User.query.get(data['developerId'])
            if not developer:
                return jsonify({"error": "Invalid developerId"}), 400

        # Validate testerId if provided
        if data.get('testerId'):
            tester = User.query.get(data['testerId'])
            if not tester:
                return jsonify({"error": "Invalid testerId"}), 400

        # Update fields only if present in the request data
        assignment.projectId = data.get('projectId', assignment.projectId)
        assignment.developerId = data.get('developerId', assignment.developerId)
        assignment.testerId = data.get('testerId', assignment.testerId)
        assignment.assignedById = data.get('assignedById', assignment.assignedById)
        assignment.title = data.get('title', assignment.title)
        assignment.desc = data.get('desc', assignment.desc)
        assignment.status = data.get('status', assignment.status)
        assignment.priority = data.get('priority', assignment.priority)

        # Handle due_date if provided
        if 'due_date' in data:
            try:
                assignment.due_date = datetime.strptime(data['due_date'], '%Y-%m-%d')
            except ValueError:
                return jsonify({"error": "Invalid due_date format. Expected YYYY-MM-DD."}), 400

        assignment.updated_at = datetime.utcnow()

        # Commit changes to the database
        db.session.commit()

        return jsonify({"message": "Assignment updated successfully"}), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Database error occurred", "details": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500

@assig_bp.route('/developer/<int:developer_id>', methods=['PUT'])
def update_assignment_by_developer(developer_id):
    data = request.get_json()  # Ensure JSON data is received

    if not data or 'assignmentId' not in data:
        return jsonify({"error": "Assignment ID is required"}), 400

    assignment_id = data.get('assignmentId')

    # Validate assignment_id is an integer
    if not isinstance(assignment_id, int):
        return jsonify({"error": "Assignment ID must be a valid integer"}), 400

    try:
        # Fetch the assignment based on the assignment_id
        assignment = Assignment.query.get(assignment_id)
        if not assignment:
            return jsonify({"message": "Assignment not found"}), 404

        # Ensure the developer making the request matches the assignment's developer
        if developer_id != assignment.developerId:
            return jsonify({"error": "Access denied. You are not authorized to update this assignment."}), 403

        # Track changes
        updated_fields = {}

        # Update allowed fields
        if 'desc' in data:
            assignment.desc = data['desc']
            updated_fields['desc'] = data['desc']
        if 'status' in data:
            assignment.status = data['status']
            updated_fields['status'] = data['status']
        if 'priority' in data:
            assignment.priority = data['priority']
            updated_fields['priority'] = data['priority']
        if 'due_date' in data:
            try:
                assignment.due_date = datetime.strptime(data['due_date'], '%Y-%m-%d')
                updated_fields['due_date'] = assignment.due_date.isoformat()
            except ValueError:
                return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

        # If any updates were made, update timestamp and commit
        if updated_fields:
            assignment.updated_at = datetime.utcnow()

        # Handle remarks separately
        if 'remark' in data:
            new_remark = Remark(
                user_id=developer_id,  
                assignment_id=assignment_id,
                remark=data['remark'],
            )
            db.session.add(new_remark)

        # Commit all changes once
        db.session.commit()

        # Serialize updated assignment
        updated_assignment = {
            "id": assignment.id,
            "projectId": assignment.projectId,
            "developerId": assignment.developerId,
            "testerId": assignment.testerId,
            "assignedById": assignment.assignedById,
            "title": assignment.title,
            "desc": assignment.desc,
            "status": assignment.status,
            "priority": assignment.priority,
            "due_date": assignment.due_date.isoformat() if assignment.due_date else None,
            "created_at": assignment.created_at.isoformat(),
            "updated_at": assignment.updated_at.isoformat(),
        }

        return jsonify({"message": "Assignment updated successfully by Developer!", "assignment": updated_assignment}), 200

    except SQLAlchemyError as e:
        db.session.rollback()  # Roll back transaction on error
        return jsonify({"error": "Database error occurred", "details": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500

# Update an assignment by tester
@assig_bp.route('/tester/<int:tester_id>', methods=['PUT'])
def update_assignment_by_tester(tester_id):
    data = request.json  # Assuming data is being sent as JSON

    try:
        # Ensure 'assignmentId' is provided in the data
        if 'assignmentId' not in data:
            return jsonify({"error": "Assignment ID is required"}), 400

        try:
            # Convert assignment_id from string to integer
            assignment_id = int(data['assignmentId'])
        except ValueError:
            return jsonify({"error": "Assignment ID must be a valid integer"}), 400

        # Fetch the assignment based on the assignment_id
        assignment = Assignment.query.get(assignment_id)
        if not assignment:
            return jsonify({"message": "Assignment not found"}), 404

        # Ensure the tester making the request matches the tester_id in the URL
        if tester_id != assignment.testerId:
            return jsonify({"error": "Access denied. You are not authorized to update this assignment."}), 403

        # Ensure the developer has updated the status first (status should not be "Pending")
        if assignment.status == "Pending":
            return jsonify({"error": "Developer has not updated the assignment status yet. You cannot update it."}), 403

        # Update allowed fields from validated data
        updated = False
        if 'desc' in data:
            assignment.desc = data['desc']
            updated = True
        if 'status' in data:
            assignment.status = data['status']
            updated = True
        if 'priority' in data:
            assignment.priority = data['priority']
            updated = True
        if 'due_date' in data:
            try:
                assignment.due_date = datetime.strptime(data['due_date'], '%Y-%m-%d')
                updated = True
            except ValueError:
                return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

        if updated:
            assignment.updated_at = datetime.utcnow()  # Update the timestamp

            # Save remark in Remarks table
            if 'remark' in data:
                new_remark = Remark(
                    user_id=tester_id,  # Assuming the tester is making the remark
                    assignment_id=assignment_id,
                    remark=data['remark'],  # Assuming 'remark' is provided in the JSON request
                    created_at=datetime.utcnow()
                )
                db.session.add(new_remark)

            # Commit the changes to the database
            db.session.commit()

        # Serialize and return the updated assignment
        updated_assignment = {
            "id": assignment.id,
            "projectId": assignment.projectId,
            "developerId": assignment.developerId,
            "testerId": assignment.testerId,
            "assignedById": assignment.assignedById,
            "title": assignment.title,
            "desc": assignment.desc,
            "status": assignment.status,
            "priority": assignment.priority,
            "due_date": assignment.due_date.isoformat() if assignment.due_date else None,
            "created_at": assignment.created_at.isoformat(),
            "updated_at": assignment.updated_at.isoformat(),
        }

        return jsonify({"message": "Assignment updated successfully by Tester!", "assignment": updated_assignment}), 200

    except SQLAlchemyError as e:
        db.session.rollback()  # Roll back the transaction in case of an error
        return jsonify({"error": "Database error occurred", "details": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500

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
