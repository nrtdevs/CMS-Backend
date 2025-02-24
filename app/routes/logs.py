from app.models.user import db, User
from app.models.logs import Log
from flask import Blueprint, request, jsonify
from app.models.logs import Log
from .token import verifyJWTToken
from user_agents import parse
from ..helper.response import success_response, error_response


logs_bp = Blueprint("logs_routes", __name__)

# Helper function to extract user-agent details
def extract_user_agent_details():
    user_agent_string = request.headers.get("User-Agent", "Unknown")
    user_agent = parse(user_agent_string)

    return {
        "browser": f"{user_agent.browser.family} {user_agent.browser.version_string}",
        "os": f"{user_agent.os.family} {user_agent.os.version_string}",
        "device": user_agent.device.family,
        "is_mobile": user_agent.is_mobile,
        "is_tablet": user_agent.is_tablet,
        "is_pc": user_agent.is_pc,
    }



def addLogsActivity(request,activity,desc):  # Accept a list of allowed user types
    ip_address = request.remote_addr or "Unknown"
    user_agent_details = extract_user_agent_details()
    logData = {
                "activity":activity,
                "desc": desc,
                "userId": request.user.id,
                "ipAddress": ip_address,
                "userAgent": user_agent_details["browser"],
                "device": user_agent_details["device"],
             }  
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
    return success_response(
        serialized_logs, "Fetched successfully paginated logs for master_admin", 200,
        {
            "total": logs.total,
            "pages": logs.pages,
            "current_page": logs.page,
            "per_page": logs.per_page,
            "has_next": logs.has_next,
            "has_prev": logs.has_prev,
        }
        )
    

