from app.extensions import db
from datetime import datetime



project_developers = db.Table(
        'project_developers',
        db.Column('project_id', db.Integer, db.ForeignKey('projects.projectId'), primary_key=True),
        db.Column('developer_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
    )   
class Project(db.Model):
    __tablename__ = 'projects'
    # Unique identifier for the project
    projectId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    currency= db.Column(db.String(80), nullable=True)
    totalBudget = db.Column(db.Integer, nullable=True)
    startDate = db.Column(db.Date, nullable=True)
    deadlineDate =db.Column(db.Date, nullable=True)
    endDate = db.Column(db.Date, nullable=True)
    status = db.Column(db.String(120), nullable=False, default='active')
    # Timestamp 
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.DateTime, nullable=True) 
   
    
   
    
    # new
    assignments_list = db.relationship(
        "Assignment",
        back_populates="project",
        cascade="all, delete-orphan",
    )
    
    # Many-to-Many relationship for developers
    developers = db.relationship('User',
       secondary=project_developers,  # Association table
       back_populates='users'
    )
    
    
     # User relation
    userId = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', foreign_keys=[userId], backref='user_details', lazy=True)
    
    # Tester relation
    techLeadId = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Optional tester
    techLead = db.relationship('User', foreign_keys=[techLeadId], backref='tester_details', lazy=True)

    # Assigner relation
    assignedById = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # User who assigned the task
    assigner = db.relationship('User', foreign_keys=[assignedById], backref='assigner_details', lazy=True)
    
    
    bidId = db.Column(db.Integer, db.ForeignKey('biddings.bidId'), nullable=False)
    bidding = db.relationship('Bidding', backref='projects', lazy=True, 
                              foreign_keys=[bidId])
    
        #developerIds relation
    # developerIds = db.Column(db.Array, db.ForeignKey('users.id'), nullable=False) 
    # developer = db.relationship('User', foreign_keys=[developerIds], backref='developer_projects', lazy=True) 
    
    # Association table for project-developer relationship
    
