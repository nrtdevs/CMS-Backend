from flask import Blueprint, request, jsonify
from app.models import Team, User, db
from cerberus import Validator


teams_bp = Blueprint('teams', __name__)

# Validator Schema
team_schema = {
    'developer_ids': {
        'type': 'list',
        'schema': {'type': 'integer'},
        'required': True
    },
    'teamLeadId': {'type': 'integer', 'required': True},
    'status': {'type': 'boolean', 'required': False},
    'teamName': {'type': 'string', 'required': True},
    'description': {'type': 'string', 'required': False},
    'techStack': {'type': 'list', 'schema': {'type': 'string'}, 'required': False}
}

team_validator = Validator(team_schema)

@teams_bp.route('/create', methods=['POST'])
def create_team():
    data = request.get_json()
    if not team_validator.validate(data):
        return jsonify({"errors": team_validator.errors}), 400

    developer_ids = data['developer_ids']
    developers = User.query.filter(User.id.in_(developer_ids)).all()

    if len(developers) != len(developer_ids):
        return jsonify({"error": 'INVALID_DEVELOPER_IDS'}), 400

    new_team = Team(
        teamName=data['teamName'],
        teamLeadId=data['teamLeadId'],
        status=data.get('status', False),
        description=data.get('description'),
        techStack=data.get('techStack', []),
        createdById=data['teamLeadId']  # Assuming the creator is the team lead
    )
    new_team.developers.extend(developers)
    db.session.add(new_team)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Integrity error occurred", "details": str(e)}), 500

    return jsonify({"message": "Team created successfully", "team_id": new_team.teamId}), 201

# Update a Team
@teams_bp.route('/update/<int:team_id>', methods=['PUT'])
def update_team(team_id):
    team = Team.query.get(team_id)
    if not team:
        return jsonify({"error": "Team not found"}), 404

    data = request.get_json()
    if 'teamName' in data:
        team.teamName = data['teamName']
    if 'teamLeadId' in data:
        team.teamLeadId = data['teamLeadId']
    if 'status' in data:
        team.status = data['status']
    if 'description' in data:
        team.description = data['description']
    if 'techStack' in data:
        team.techStack = data['techStack']

    # Handle the developer updates if necessary
    if 'developer_ids' in data:
        developer_ids = data['developer_ids']
        developers = User.query.filter(User.id.in_(developer_ids)).all()

        if len(developers) != len(developer_ids):
            return jsonify({"error": 'INVALID_DEVELOPER_IDS'}), 400

        # Clear existing developers and add the new ones
        team.developers.clear()
        team.developers.extend(developers)

    db.session.commit()
    return jsonify({"message": 'TEAM_UPDATE_SUCCESS'}), 200

# Get all teams
@teams_bp.route('/get_all', methods=['GET'])
def get_all_teams():
    teams = Team.query.all()
    return jsonify([team.to_dict() for team in teams]), 200

# Get teams By Id
@teams_bp.route('/<int:team_id>', methods=['GET'])
def get_team_by_id(team_id):
    team = Team.query.get(team_id)
    print(team)
    user = User.query.get(team_id) if team_id else None
    if not team:
        return jsonify({"error": 'TEAM_NOT_FOUND'}), 404

    team_data = team.to_dict()
    print(team_data)
    
    team_data['created_at'] = team.created_at.isoformat()  # 
    team_data['created_by'] = { "id" :user.id,
                               "Firstname":user.firstName,
                               "lastName":user.lastName}
    team_data['updated_at'] = team.updated_at.isoformat()  # 
    team_data['developers'] = [developer.to_dict() for developer in team.developers]

    return jsonify(team_data), 200

