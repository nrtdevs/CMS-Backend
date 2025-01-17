from datetime import datetime
from app.extensions import db

# Association Table for many-to-many relationship between Team and User
team_users = db.Table('Team_developer_id',
    db.Column('team_id', db.Integer, db.ForeignKey('teams.team_id'), primary_key=True),
    db.Column('developer_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
)

class Team(db.Model):
    __tablename__ ='teams'
    
    team_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    teamlead_Id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.Boolean, default=False)
     # Timestamps
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.DateTime, nullable=True)
    

    # Many-to-Many Relationship with User
    developers = db.relationship('User', secondary=team_users, back_populates='teams')
    # Relationships
    team_lead = db.relationship('User', foreign_keys=[teamlead_Id], backref='leading_teams', lazy=True)
    


    # Project relationship
    projects = db.relationship(
        "Project",
        back_populates="team",
        cascade="all, delete-orphan"
    )
    
    
    def to_dict(self):
        return {
            'team_id': self.team_id,
            'teamlead_Id': self.teamlead_Id,
            'status': self.status,
            'developer_ids': [developer.id for developer in self.developers]
        }