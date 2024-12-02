# api/endpoints.py
from flask import Blueprint, jsonify, request
from services.google_ads_client import get_google_ads_client
from services.google_ads_service import get_accessible_customers

api_bp = Blueprint('api', __name__)

@api_bp.route('/accessible-customers', methods=['GET'])
def accessible_customers():
    login_customer_id = request.args.get('login_customer_id')
    if not login_customer_id:
        return jsonify({"error": "login_customer_id is required"}), 400

    client = get_google_ads_client()
    customers = get_accessible_customers(client)
    return jsonify(customers)