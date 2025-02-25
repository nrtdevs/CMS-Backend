from flask import Blueprint, request, jsonify
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import IntegrityError
from cerberus import Validator
from datetime import datetime
from .token import verifyJWTToken
from app.models.user import User, db
from app.models.project import Project, db
from ..helper.response import success_response, error_response

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
    try:
        project = (
            db.session.query(Project)
            .filter_by(projectId=projectId)
            .first()
        )
        if not project:
            return error_response('Project not found', "Project_id not found", 404)
           

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

        return success_response(project_data, "Project fetched successfully", 200)
    except Exception as e:
        return error_response("Internal server error", str(e), 500)

projects_bp = Blueprint('projects', __name__)
@projects_bp.route('/list', methods=['GET'])
@verifyJWTToken(['master_admin', 'user'])  # Ensures the user is authenticated with specific roles
def get_all_projects():
    """Fetch all projects with optional filters, pagination, and relationships."""
    try:
        # Get search parameters
        project_name = request.args.get('projectName', default=None, type=str)
        status = request.args.get('status', default=None, type=str)
        # Pagination parameters
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=10, type=int)

        # Validate project_name if required
        if project_name is not None and not project_name.strip():
            return error_response("Project name cannot be empty", "Project name cannot be empty", 400)
        
        # Base query with relationships loaded
        query = db.session.query(Project).options(
            joinedload(Project.developers),
            joinedload(Project.techLead)
        )
        # Apply filters if provided
        if project_name:
            query = query.filter(Project.projectName.ilike(f"%{project_name}%"))
        if status:
            query = query.filter(Project.status.ilike(f"%{status}%"))

        # Paginate results
        paginated_projects = query.paginate(page=page, per_page=per_page, error_out=False)
        
        # Serialize the project data
        projects_data = [
            {
                "projectId": project.projectId,
                "projectName": project.projectName,
                "currency": project.currency,
                "totalBudget": project.totalBudget,
                "startDate": project.startDate,
                "deadlineDate": project.deadlineDate,
                "status": project.status,
                "created_at": project.created_at,
                "assignments_list": [
                    {
                        "assignmentId": assignment.id,
                        "title": assignment.title,
                        "desc": assignment.desc,
                        "status": assignment.status,
                        "created_at": assignment.created_at,
                        "updated_at": assignment.updated_at,
                    }
                    for assignment in project.assignments_list
                ],
                "developers": [
                    {"id": developer.id, "name": f"{developer.firstName} {developer.lastName}"}
                    for developer in project.developers
                ],
                "techLead": {
                    "id": project.techLead.id,
                    "name": f"{project.techLead.firstName} {project.techLead.lastName}"
                } if project.techLead else None,
            }
            for project in paginated_projects.items
        ]
        
        # Check if no projects were found
        if not projects_data:
            return error_response("No projects found. Please refine your search criteria.", "No projects found. Please refine your search criteria.", 404)

        # Return response
        return success_response(projects_data, "Projects fetched successfully", 200, 
            {
                "page": paginated_projects.page,
                "per_page": paginated_projects.per_page,
                "total_pages": paginated_projects.pages,
                "total_items": paginated_projects.total,
            })
    except Exception as e:
        return error_response("Internal server error", str(e), 500)




