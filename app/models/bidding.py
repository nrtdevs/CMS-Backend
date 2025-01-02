from app.extensions import db
from datetime import datetime


class Bidding(db.Model):
    __tablename__ = 'biddings'
    
    # Unique identifier for the project
    bidId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    projectName = db.Column(db.String(80), nullable=False)
    projectDescription = db.Column(db.String(300), nullable=True)  # Limited to 300 characters
    skills = db.Column(db.String(80), nullable=False)
    currency= db.Column(db.String(80), nullable=True)
    
    bidAmount = db.Column(db.Integer, nullable=True)
    platform = db.Column(db.String(80), nullable=False)
    bidDate = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    uploadUrl = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    status = db.Column(db.String(120), nullable=False, default='pending')
    clientName = db.Column(db.String(80), nullable=False)
    clientEmail = db.Column(db.String(120), unique=True, nullable=False)
    clientContact = db.Column(db.Integer, unique=True, nullable=False)
    clientCompany = db.Column(db.String(120), nullable=True)
    clientLocation = db.Column(db.String(120), nullable=True)
    remarks = db.Column(db.Text, nullable=True)
    
    userId = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    projectId = db.Column(db.Integer, db.ForeignKey('projects.projectId'), nullable=True)

    # Relationships
    user = db.relationship('User', back_populates='biddings')
    project = db.relationship('Project', back_populates='bidding', uselist=False)

 
    
    
  
