from flask import Blueprint, request, jsonify
from app.models.user import User, db
from sqlalchemy.exc import IntegrityError
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, NumberRange, Email
from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Needed for Flask-WTF CSRF protection

class RegisterForm(FlaskForm):
    firstName = StringField('firstName', validators=[DataRequired(), Length(min=2, max=50)])
    lastName = StringField('lastName', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('email', validators=[DataRequired(), Length(min=2, max=50), Email(message="Invalid email address.")])
    password = PasswordField('password', validators=[DataRequired(), Length(min=8, max=50)])
    countryCode = StringField('countryCode', validators=[DataRequired(), Length(min=2, max=50)])
    mobileNo = IntegerField('mobileNo', validators=[DataRequired(), Length(min=2, max=50)])
    empID = IntegerField('empID', validators=[DataRequired(), Length(min=2, max=50)])
    role = StringField('role', validators=[DataRequired(), Length(min=2, max=50)])
    userType = StringField('userType', validators=[DataRequired(), Length(min=2, max=50)])
    
    


users_bp = Blueprint('user_routes', __name__)

# CREATE user
@users_bp.route('/register', methods=['POST'])
def create_user():
    data = request.get_json()
    form = RegisterForm(data=data)
    
    firstName = form.firstName.data
    email = form.email.data
    
    
    if form.validate():
        
        
        # userCheck=User.findOne({
        #     email:email,
        #     status:True
        # })
        # if(userCheck){
        #     return jsonify({'message': 'User created', 'id': new_user.id}),400 
            
        # }
        try:         
            new_user = User(firstName=firstName, email=email)
            db.session.add(new_user)
            db.session.commit()
            return jsonify({'message': 'User created', 'id': new_user.id}), 201
        except IntegrityError:
            db.session.rollback()
            return jsonify({'error': 'User with this email already exists'}), 400
    else:
        return jsonify({'errors': form.errors}), 400

# READ all users
@users_bp.route('/users', methods=['GET'])
def get_users():
    0
    
    users = User.query.all()
    users_list = [{"id": user.id, "name": user.name, "email": user.email} for user in users]
    return jsonify(users_list)

# READ a single user
@users_bp.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({"id": user.id, "name": user.name, "email": user.email})

# UPDATE user
@users_bp.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.get_json()
    
    

    user = User.query.get(id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    user.name = data.get('name', user.name)
    user.email = data.get('email', user.email)
    user.password = data.get('password', user.password)
    
    db.session.commit()
    return jsonify({"message": "User updated"})

# DELETE user
@users_bp.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted'}), 200


