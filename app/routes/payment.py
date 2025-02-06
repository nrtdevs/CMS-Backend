from sqlalchemy.orm import joinedload
from flask import Blueprint, request, jsonify
from app.models.payment import Payment, db
from app.models.project import Project
from app.extensions import db
from datetime import datetime
from cerberus import Validator

payments_bp = Blueprint('payment_routes', __name__)

payment_schema = {
    'amount': {'type': 'float', 'required': True},
    'currency': {'type': 'string', 'maxlength': 10, 'required': True},
    'payment_method': {'type': 'string', 'maxlength': 50, 'required': True},
    'status': {'type': 'string', 'maxlength': 50, 'required': True},
    'transaction_id': {'type': 'string', 'maxlength': 100, 'required': False},
    'description': {'type': 'string', 'maxlength': 255, 'required': False},
    'payer_name': {'type': 'string', 'maxlength': 100, 'required': False},
    'payer_email': {'type': 'string', 'regex': r'^[^@]+@[^@]+\.[^@]+$', 'required': False},
    'payment_provider': {'type': 'string', 'maxlength': 50, 'required': False},
    'receipt_url': {'type': 'string', 'maxlength': 255, 'required': False},
    'project_id': {'type': 'integer', 'required': True}
}

validator = Validator(payment_schema)

# CREATE Payment


@payments_bp.route('/create', methods=['POST'])
def create_payment():
    data = request.get_json()

    # Validate the input data
    if not validator.validate(data):
        return jsonify({"errors": validator.errors}), 400

    # Check if project exists
    project = Project.query.filter_by(projectId=data['project_id']).first()
    if not project:
        return jsonify({"error": "Project not found"}), 404

    try:
        payment = Payment(**data)
        db.session.add(payment)
        db.session.commit()

        payment_data = {
            "id": payment.id,
            "amount": payment.amount,
            "currency": payment.currency,
            "payment_date": payment.payment_date,
            "payment_method": payment.payment_method,
            "status": payment.status,
            "transaction_id": payment.transaction_id,
            "description": payment.description,
            "payer_name": payment.payer_name,
            "payer_email": payment.payer_email,
            "payment_provider": payment.payment_provider,
            "receipt_url": payment.receipt_url,
            "refunded": payment.refunded,
            "refund_date": payment.refund_date,
            "project_id": payment.project_id
        }
        return jsonify({"message": "Payment created successfully", "data": payment_data}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error creating payment", "details": str(e)}), 500

# READ Single Payment


@payments_bp.route('/<int:id>', methods=['GET'])
def get_payment(id):
    payment = Payment.query.filter_by(id=id).first()
    if not payment:
        return jsonify({"error": "Payment not found"}), 404

    payment_data = {
        "id": payment.id,
        "amount": payment.amount,
        "currency": payment.currency,
        "payment_date": payment.payment_date,
        "payment_method": payment.payment_method,
        "status": payment.status,
        "transaction_id": payment.transaction_id,
        "description": payment.description,
        "payer_name": payment.payer_name,
        "payer_email": payment.payer_email,
        "payment_provider": payment.payment_provider,
        "receipt_url": payment.receipt_url,
        "refunded": payment.refunded,
        "refund_date": payment.refund_date,
        "project_id": payment.project_id
    }
    return jsonify({"message": "Payment fetched successfully", "data": payment_data}), 200


@payments_bp.route('/all', methods=['GET'])
def get_payments():
    # Get the page, per_page, and filter parameters from the request
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)
    search_query = request.args.get('search', default='', type=str)
    status_filter = request.args.get('status', default='', type=str)
    project_name = request.args.get('project_name', default=None, type=str)

    # Start the query and join with the Project table based on project_id
    query = Payment.query.join(Project, Payment.project_id == Project.projectId).options(
        joinedload(Payment.project),  # Eager load the user relationship
        joinedload(Payment.project)  # Eager load the project relationship
    )

    # Apply project_name filter if a project_name is provided
    if project_name:
        # Perform a case-insensitive search for project names
        search_filter = f"%{project_name}%"
        query = query.filter(Project.projectName.ilike(search_filter))

    # Apply search filter if a search term is provided (search across payer_name, transaction_id, etc.)
    if search_query:
        search_filter = f"%{search_query}%"
        query = query.filter(
            (Payment.payer_name.ilike(search_filter)) |
            (Payment.transaction_id.ilike(search_filter)) |
            (Payment.description.ilike(search_filter))
        )

    # Apply status filter if a status is provided
    if status_filter:
        query = query.filter(Payment.status == status_filter)

    # Apply pagination
    paginated_payments = query.paginate(
        page=page, per_page=per_page, error_out=False)

    # Prepare the list of payments to be returned
    payments_list = [
        {
            "id": payment.id,
            "amount": payment.amount,
            "currency": payment.currency,
            "payment_date": payment.payment_date,
            "payment_method": payment.payment_method,
            "status": payment.status,
            "transaction_id": payment.transaction_id,
            "description": payment.description,
            "payer_name": payment.payer_name,
            "payer_email": payment.payer_email,
            "payment_provider": payment.payment_provider,
            "receipt_url": payment.receipt_url,
            "refunded": payment.refunded,
            "refund_date": payment.refund_date,
            "project_id": payment.project_id,
            "project_name": payment.project.projectName,  # Add project name to the response
            "user": {
                "id": payment.project.project_id,
                "firstName": payment.project.first_name,
                "lastName": payment.project.last_name,
                "role": payment.project.role
            } if payment.project else None  # Include project information if it exists
        }
        for payment in paginated_payments.items
    ]

    # Check if no payments were found
    if not payments_list:
        return jsonify({
            "error": "No payments found. Please refine your search criteria."
        }), 404

    # Return the response with pagination info
    return jsonify({
        "message": "Payments fetched successfully",
        "data": payments_list,
        "pagination": {
            "page": paginated_payments.page,
            "per_page": paginated_payments.per_page,
            "total_pages": paginated_payments.pages,
            "total_items": paginated_payments.total,
        }
    }), 200


# UPDATE Payment
@payments_bp.route('/update/<int:id>', methods=['PUT'])
def update_payment(id):
    data = request.get_json()
    payment = Payment.query.filter_by(id=id).first()

    if not payment:
        return jsonify({"error": "Payment not found"}), 404

    # Update payment fields
    for key, value in data.items():
        if hasattr(payment, key):
            setattr(payment, key, value)

    db.session.commit()

    return jsonify({"message": "Payment updated successfully"}), 200

# DELETE Payment


@payments_bp.route('/delete/<int:id>', methods=['DELETE'])
def delete_payment(id):
    payment = Payment.query.filter_by(id=id).first()

    if not payment:
        return jsonify({"error": "Payment not found"}), 404

    db.session.delete(payment)
    db.session.commit()

    return jsonify({"message": "Payment deleted successfully"}), 200
