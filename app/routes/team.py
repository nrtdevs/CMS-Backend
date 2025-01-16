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
    'teamlead_Id': {'type': 'integer', 'required': True},
    'status': {'type': 'boolean', 'required': False},
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
        return jsonify({"error": "Some developer IDs are invalid"}), 400

    new_team = Team(
        teamlead_Id=data['teamlead_Id'],
        status=data.get('status', False)
    )
    new_team.developers.extend(developers)
    db.session.add(new_team)
    
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Integrity error occurred", "details": str(e)}), 500

    return jsonify({"message": "Team created successfully", "team_id": new_team.team_id}), 201

# Update a Team
@teams_bp.route('/update/<int:team_id>', methods=['PUT'])
def update_team(team_id):
    team = Team.query.get(team_id)
    if not team:
        return jsonify({"error": "Team not found"}), 404

    data = request.get_json()
    if 'teamlead_Id' in data:
        team.teamlead_Id = data['teamlead_Id']
    if 'status' in data:
        team.status = data['status']

    # Handle the developer updates if necessary
    if 'developer_ids' in data:
        developer_ids = data['developer_ids']
        developers = User.query.filter(User.id.in_(developer_ids)).all()

        if len(developers) != len(developer_ids):
            return jsonify({"error": "Some developer IDs are invalid"}), 400

        # Clear existing developers and add the new ones
        team.developers.clear()
        team.developers.extend(developers)

    db.session.commit()
    return jsonify({"message": "Team updated successfully"}), 200


#Get all teams
@teams_bp.route('/get_all', methods=['GET'])
def get_all_teams():
    teams = Team.query.all()
    return jsonify([team.to_dict() for team in teams]), 200


#Get teams By Id
@teams_bp.route('/<int:team_id>', methods=['GET'])
def get_team_by_id(team_id):
    team = Team.query.get(team_id)
    if not team:
        return jsonify({"error": "Team not found"}), 404
    return jsonify(team.to_dict()), 200

