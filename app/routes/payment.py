from collections import defaultdict
from sqlalchemy import func
from sqlalchemy.orm import joinedload
from flask import Blueprint, request, jsonify
from app.models.payment import Payment, db
from app.models.project import Project
from app.extensions import db
from datetime import datetime
from cerberus import Validator
from ..helper.response import success_response, error_response


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
        return error_response("Invalid data", str(validator.errors), 400)

    # Check if project exists
    project = Project.query.filter_by(projectId=data['project_id']).first()
    if not project:
        return error_response("Project_id not found", "Project_id not found", 404)

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
        return success_response(payment_data, "Payment created successfully", 201)

    except Exception as e:
        db.session.rollback()
        return error_response("Integrity Error creating payment", str(e), 500)

# READ Single Payment


@payments_bp.route('/<int:id>', methods=['GET'])
def get_payment(id):
    try:
        payment = Payment.query.filter_by(id=id).first()
        if not payment:
            return error_response("Payment not found", "Payment_id not found", 404)

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


# Read All Payments
@payments_bp.route('/all', methods=['GET'])
def get_payments():
    # Get query parameters
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)
    search_query = request.args.get('search', default='', type=str)
    status_filter = request.args.get('status', default='', type=str)
    project_name = request.args.get('project_name', default=None, type=str)

    # Query payments and join with projects
    query = Payment.query.join(Project, Payment.project_id == Project.projectId).options(
        joinedload(Payment.project)  # Eager load project relationship
    )

    # Apply project name filter
    if project_name:
        search_filter = f"%{project_name}%"
        query = query.filter(Project.projectName.ilike(search_filter))

    # Apply search filters
    if search_query:
        search_filter = f"%{search_query}%"
        query = query.filter(
            (Payment.payer_name.ilike(search_filter)) |
            (Payment.transaction_id.ilike(search_filter)) |
            (Payment.description.ilike(search_filter))
        )

    # Apply status filter
    if status_filter:
        query = query.filter(Payment.status == status_filter)

    # Paginate results
    paginated_payments = query.paginate(
        page=page, per_page=per_page, error_out=False)

    # Prepare the response data
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
            "project_id": payment.project.projectId if payment.project else None,
            "project_name": payment.project.projectName if payment.project else None,
            "user": {
                "id": payment.project.user.id,
                "firstName": payment.project.user.firstName,
                "lastName": payment.project.user.lastName,
                "role": str(payment.project.user.role)  # Convert to string
            } if payment.project and payment.project.user else None
        }
        for 
        ]
        return success_response(payment_data, "Payment fetched successfully", 200)
    except Exception as e:
        return error_response("Internal server error", str(e), 500)

    # Return response
    return jsonify({
        "message": "Payments fetched successfully" if payments_list else "No payments found.",
        "data": payments_list,
        "pagination": {
            "page": paginated_payments.page,
            "per_page": paginated_payments.per_page,
            "total_pages": paginated_payments.pages,
            "total_items": paginated_payments.total,
        }
    }), 200 if payments_list else 404


# Summary
@payments_bp.route('/summary', methods=['GET'])
def get_payment_summary():
    """
    Fetches all payments and provides:
    - Total sum of payments.
    - Number of times payments were made for each project.
    - Total amount paid for each project.
    - Supports filtering by date range, user ID, and project ID.
    """

    def parse_date(date_str):
        try:
            return datetime.strptime(date_str, "%Y-%m-%d")
        except (ValueError, TypeError):
            return None

    start_date = parse_date(request.args.get('start_date'))
    end_date = parse_date(request.args.get('end_date'))
    user_id = request.args.get('user_id', type=int)
    project_id = request.args.get('project_id', type=int)

    if (start_date and not end_date) or (end_date and not start_date):
        return jsonify({"error": "Both start_date and end_date must be provided."}), 400

    query = db.session.query(Payment)

    if start_date and end_date:
        query = query.filter(Payment.payment_date.between(start_date, end_date))
    if user_id:
        query = query.filter(Payment.user_id == user_id)
    if project_id:
        query = query.filter(Payment.project_id == project_id)

    all_payments = query.all()
    total_sum = db.session.query(func.sum(Payment.amount)).scalar() or 0

    project_payment_data = defaultdict(lambda: {"name": None, "count": 0, "total_payment": 0.0, "currency": None, "total_budget": 0.0})

    for payment in all_payments:
        if payment.project:
            pid = payment.project_id
            project_payment_data[pid]["name"] = payment.project.projectName
            project_payment_data[pid]["count"] += 1
            project_payment_data[pid]["total_payment"] += float(payment.amount)
            project_payment_data[pid]["currency"] = payment.currency
            project_payment_data[pid]["total_budget"] = payment.project.total_budget if hasattr(payment.project, 'total_budget') else 0.0

    return jsonify({
        "message": "Payments fetched successfully",
        "total_sum": float(total_sum),
        "total_payments": len(all_payments),
        "payments_per_project": [
            {
                "project_id": pid,
                "project_name": pdata["name"],
                "payment_count": pdata["count"],
                "total_payment": round(pdata["total_payment"], 2),
                "currency": pdata["currency"],
                "total_budget": round(pdata["total_budget"], 2)
            }
            for pid, pdata in project_payment_data.items()
        ]
    }), 200
