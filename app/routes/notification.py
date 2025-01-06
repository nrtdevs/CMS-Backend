from flask import Flask,jsonify,request
from datetime import datetime
from app.models import Notification,db
from flask import Blueprint, request, jsonify

notification_bp = Blueprint('notification', __name__)

def create_notification(notifyData):
    
    try:
        new_notification = Notification(**notifyData) 
        db.session.add(new_notification)
        db.session.commit()
        print("Success to Notify")
    except Exception as e:
        print("Failed to Notify")
        
@notification_bp.route('/<int:user_id>', methods=['GET'])
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
                "created_at": n.created_at.isoformat(),
                "updated_at": n.updated_at.isoformat(),
                "deleted_at": n.deleted_at.isoformat() if n.deleted_at else None
            }
            for n in notifications
        ]

        return jsonify({
            "status": "success",
            "data": notification_list
        }), 200

    except Exception as e:
        # Handle errors
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
