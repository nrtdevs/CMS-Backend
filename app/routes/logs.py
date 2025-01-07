from app.models.user import db, User
from app.models.logs import Log
from flask import Blueprint, request, jsonify
from app.models.logs import Log
from .token import verifyJWTToken

logs_bp = Blueprint("logs_routes", __name__)

# Function to log activity
def createActivityLogs(logData):  
    try:
        new_log = Log(**logData)
        db.session.add(new_log)
        db.session.commit()
        print("Success to logs")   
    except Exception as e:
        print("Failed to logs",e)
    
@logs_bp.route('/', methods=['GET'])
@verifyJWTToken(['master_admin'])  # Restrict to master_admin
def get_logs():
    """
    Fetch paginated logs (only for master_admin users).
    Query Parameters:
        page (int): The page number (default: 1).
        per_page (int): Number of items per page (default: 10).
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    # Fetch logs with pagination
    logs = Log.query.paginate(page=page, per_page=per_page, error_out=False)

    # Serialize logs
    serialized_logs = [
        {
            "id": log.id,
            "activity": log.activity,
            "desc": log.desc,
            "userId": log.userId,
            "ipAddress": log.ipAddress,
            "userAgent": log.userAgent,
            "device": log.device,
            "created_at": log.created_at.isoformat(),
            "serialized_user": log.serialized_user,  # Include serialized user details

            
        }
        for log in logs.items
    ]
    
    

    # Return paginated data
    return jsonify({
        "logs": serialized_logs,
        "total": logs.total,
        "pages": logs.pages,
        "current_page": logs.page,
        "per_page": logs.per_page,
        "has_next": logs.has_next,
        "has_prev": logs.has_prev,
    }), 200 
    




