from app.extensions import db
from datetime import datetime

class Project(db.Model):
    __tablename__ = 'projects'
    # Unique identifier for the project
    projectId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    currency= db.Column(db.String(80), nullable=True)
    totalBudget = db.Column(db.Integer, nullable=True)
    frontDev = db.Column(db.JSON, nullable=True)  # JSON to store arrays
    backDev = db.Column(db.JSON, nullable=True)   # JSON to store arrays
    teachLead = db.Column(db.JSON, nullable=True) # JSON to store arrays
    tester = db.Column(db.JSON, nullable=True)     # Array of strings
    uploadUrl = db.Column(db.String(255), nullable=True)
    startDate = db.Column(db.Date, nullable=True)
    deadlineDate =db.Column(db.Date, nullable=True)
    endDate = db.Column(db.Date, nullable=True)
    status = db.Column(db.String(120), nullable=False, default='active')
    approvedBy = db.Column(db.String(255), default='user') 
    # Timestamp 
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.DateTime, nullable=True) 
    # relationship
    userId = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    bidId = db.Column(db.Integer, db.ForeignKey('biddings.bidId'), nullable=False)
    
    user = db.relationship('User', backref='projects', lazy=True)
    bidding = db.relationship('Bidding', backref='projects', lazy=True, 
                              foreign_keys=[bidId])