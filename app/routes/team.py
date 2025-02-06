from flask import Blueprint, request, jsonify
from app.models import Team, User, db
from cerberus import Validator
from .token import verifyJWTToken


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
@verifyJWTToken(['master_admin','user'])
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

    return jsonify({
        "message": "Team created successfully",
        "team": {
            "teamId": new_team.teamId,
            "teamName": new_team.teamName,
            "teamLeadId": new_team.teamLeadId,
            "status": new_team.status,
            "description": new_team.description,
            "techStack": new_team.techStack,
            "createdById": new_team.createdById,
            "developer_ids": [dev.id for dev in new_team.developers]
        }
    }), 201


# Update a Team
@teams_bp.route('/update/<int:team_id>', methods=['PUT'])
@verifyJWTToken(['master_admin','user'])
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
@verifyJWTToken(['master_admin','user'])
def get_all_teams():
    teams = Team.query.all()
    return jsonify({
        "message": "All Teams Fetched successfully",
        "teams": [
            {
                "teamId": team.teamId,
                "teamName": team.teamName,
                "teamLeadId": team.teamLeadId,
                "status": team.status,
                "description": team.description,
                "techStack": team.techStack,
                "createdById": team.createdById,
                "developer_ids": [dev.id for dev in team.developers]
            }
            for team in teams
        ]
    }), 200


# Get teams By Id
@teams_bp.route('/<int:team_id>', methods=['GET'])
@verifyJWTToken(['master_admin','user'])
def get_team_by_id(team_id):
    # Fetch team by ID
    team = Team.query.get(team_id)
    if not team:
        return jsonify({"error": "TEAM_NOT_FOUND"}), 404

    # Fetch user (creator of the team)
    user = User.query.get(team.createdById) if team.createdById else None

    # Construct response data
    team_data = {
        "teamId": team.teamId,
        "teamName": team.teamName,
        "teamLeadId": team.teamLeadId,
        "status": team.status,
        "description": team.description,
        "techStack": team.techStack,
        "created_at": team.created_at.isoformat() if team.created_at else None,
        "updated_at": team.updated_at.isoformat() if team.updated_at else None,
        "created_by": {
            "id": user.id if user else None,
            "firstName": user.firstName if user else None,
            "lastName": user.lastName if user else None
        },
        "developers": [
            {
                "id": developer.id,
                "firstName": developer.firstName,
                "lastName": developer.lastName
            } for developer in team.developers
        ]
    }

    return jsonify(team_data), 200
