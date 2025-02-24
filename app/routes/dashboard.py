from flask import Blueprint, request, jsonify
from app.models.bidding import Bidding, db
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import IntegrityError
from cerberus import Validator
from datetime import datetime
from .token import verifyJWTToken
from app.models.user import User, db
from app.models.project import Project, db
from ..helper.response import success_response, error_response



dashboard_bp = Blueprint('dashbord_routes', __name__)


@dashboard_bp.route('/get', methods=['GET'])
def get_dashboard_data():
    
    # Module name for User module (could be static or dynamic if you store module names)
    user_module_name = "User Module"
     
    # --- From User Module ---
    total_users = User.query.count()  # Total users
    active_users = User.query.filter_by(status=True).count()  # Active users

   
   # Module name for Bidding module
    bidding_module_name = "Bidding Module"
    # --- From Bidding Module ---
    total_biddings = Bidding.query.count()  # Total biddings
    approved_biddings = Bidding.query.filter_by(status='approved').count()  # Approved biddings

    
    # Module name for Project module
    project_module_name = "Project Module"
    # --- From Project Module ---
    pending_projects = Project.query.filter_by(status='pending').count()  # Pending projects
    active_projects = Project.query.filter_by(status='active').count()  # Active projects

    

    # Compiling the dashboard data
    dashboard_data = {
        'user_module': {
            'module_name': user_module_name,
            'total_users': total_users,
            'active_users': active_users
            
        },
        'bidding_module': {
            'module_name': bidding_module_name,
            'total_biddings': total_biddings,
            'approved_biddings': approved_biddings
            
        },
        'project_module': {
            'module_name': project_module_name,
            'pending_projects': pending_projects,
            'active_projects': active_projects,
            
        }
    }

    return success_response(dashboard_data, "", 200)
