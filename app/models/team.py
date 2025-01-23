from datetime import datetime
from app.extensions import db

# Association Table for many-to-many relationship between Team and User
team_users = db.Table('Team_developer_id',
    db.Column('teamId', db.Integer, db.ForeignKey('teams.teamId'), primary_key=True),
    db.Column('developer_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
)

class Team(db.Model):
    __tablename__ ='teams'
    
    teamId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    teamName = db.Column(db.String(255), nullable=False)
    teamLeadId = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.Boolean, default=False)
    createdById = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # User who created the team
    description = db.Column(db.Text, nullable=True)
    techStack = db.Column(db.JSON, nullable=True)

     # Timestamps
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.DateTime, nullable=True)
    

    # Many-to-Many Relationship with User
    developers = db.relationship('User', secondary=team_users, back_populates='teams')
    # Relationships
    team_lead = db.relationship('User', foreign_keys=[teamLeadId], backref='leading_teams', lazy=True)
    created_by_user = db.relationship('User', foreign_keys=[createdById], backref='created_teams', lazy=True)
    

    # Project relationship
    projects = db.relationship(
        "Project",
        back_populates="team",
        cascade="all, delete-orphan"
    )
    
    
    def to_dict(self):
        return {
            'team_id': self.teamId,
            'team_name': self.teamName,  # Include team name in the dictionary
            'teamlead_Id': self.teamLeadId,
            'created_by': self.createdById,  # Include created_by user ID in the dictionary
            'description': self.description,  # Include description in the dictionary
            'status': self.status,
            'tech_stack': self.techStack,
            'developer_ids': [developer.id for developer in self.developers]   }
