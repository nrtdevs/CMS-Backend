from app.extensions import db
from datetime import datetime

class Assignment(db.Model):
    __tablename__ = 'assignments'

    # Primary Key
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # Task details
    title = db.Column(db.String(100), nullable=False)  # Task title or brief summary
    desc = db.Column(db.Text, nullable=False)  # Detailed task description
    status = db.Column(db.String(50), nullable=False, default='Pending')  # Task status
    priority = db.Column(db.String(20), nullable=False, default='Medium')  # Task priority: Low, Medium, High
    due_date = db.Column(db.DateTime, nullable=True)  # Optional due date for the task

    # Timestamps
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # def __repr__(self):
    #     return f"<Assignment(id={self.id}, title='{self.title}', status='{self.status}', priority='{self.priority}', assignedBy={self.assignedBy})>"

    # project relation
    projectId = db.Column(db.Integer, db.ForeignKey('projects.projectId'), nullable=False)  # Links to the project
    project = db.relationship('Project', back_populates='assignments_list')
    
    # Developer relation
    developerId = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    developer = db.relationship('User', foreign_keys=[developerId], backref='developer_assignments', lazy=True)

    # Tester relation
    testerId = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # Optional tester
    tester = db.relationship('User', foreign_keys=[testerId], backref='tester_assignments', lazy=True)

    # Assigner relation
    assignedById = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # User who assigned the task
    assigner = db.relationship('User', foreign_keys=[assignedById], backref='assigner_assignments', lazy=True)