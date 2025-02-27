from flask import Flask,jsonify,request
from datetime import datetime
from app.models import Notification,db
from flask import Blueprint, request, jsonify
from .token import verifyJWTToken
from ..helper.response import success_response, error_response

notification_bp = Blueprint('notification', __name__)

def create_notification(notifyData): 
    try:
        from app.database import socketio
        
        new_notification = Notification(**notifyData) 
        db.session.add(new_notification)
        db.session.commit()

        print("✅ Success to Notify")

        # 🔥 Emit the notification event to all connected clients
        socketio.emit('new_notification', notifyData)
        
    except Exception as e:
        print("❌ Error:", e)
        db.session.rollback()
        print("⚠️ Failed to Notify")
        
@notification_bp.route('/<int:user_id>', methods=['GET'])
@verifyJWTToken(['master_admin','user'])
def get_notifications_by_user_id(user_id):
    try:
        # Query notifications by user_id
        notifications = Notification.query.filter_by(user_id=user_id).all()

        # Format the notifications into a list of dictionaries
        notification_list = [
            {
                "id": n.id,
                "user_id": n.user_id,
                "message": n.message,
                "module": n.module,
                "seen": n.seen,
                "subject":n.subject,
                "url":n.url,
                "created_at": n.created_at.isoformat(),
                "updated_at": n.updated_at.isoformat(),
                "deleted_at": n.deleted_at.isoformat() if n.deleted_at else None,
                "read_at":n.read_at.isoformat()
            }
            for n in notifications
        ]

        return success_response(notification_list, "Successfully feched notification", 200)
            
    except Exception as e:
        # Handle errors
        return error_response("Internal serever error", str(e), 500)
            

@notification_bp.route('/mark_as_read/<int:notification_id>', methods=['PUT'])
@verifyJWTToken(['master_admin','user'])
def mark_notification_as_read(notification_id):
    try:
        # Find the notification by id
        notification = Notification.query.filter_by(id=notification_id).first()

        if notification is None:
            return error_response("Notification not found", "Notification not found", 404)
        

        # Update the 'seen' field to True
        notification.seen = True
        notification.updated_at = datetime.utcnow()
        notification.read_at = datetime.utcnow()

        # Commit the changes to the database
        db.session.commit()

        return success_response({}, "Notification marked as read", 200)
            
    except Exception as e:
        db.session.rollback()
        # Handle errors
        return error_response("Database error", str(e), 500)
            


# Define the route for marking all notifications as read
@notification_bp.route('/mark_all_as_read/<int:user_id>', methods=['PUT'])
@verifyJWTToken(['master_admin','user'])
def mark_all_notifications_as_read(user_id):
    try:
        # Query notifications by user_id that are not yet seen
        notifications = Notification.query.filter_by(user_id=user_id, seen=False).all()

        if not notifications:
            return success_response({},"No unread notifications found", 200)
                

        # Update the 'seen' field to True for all notifications
        for notification in notifications:
            notification.seen = True
            notification.updated_at = datetime.utcnow()  # Update the timestamp
            notification.read_at = datetime.utcnow()

        # Commit the changes to the database
        db.session.commit()

        return success_response({}, f"All notifications for user {user_id} marked as read", 200)
            

    except Exception as e:
        # Handle errors
        return error_response("Internal server error", str(e), 500)
            
