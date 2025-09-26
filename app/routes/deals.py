from flask import request, jsonify, Blueprint
from .. import db
from ..models import Deal, Property, User
from flask_jwt_extended import jwt_required, get_jwt_identity

deals_bp = Blueprint('deals', __name__, url_prefix='/deals')

@deals_bp.route('/', methods=['POST'])
@jwt_required()
def initiate_deal():
    data = request.get_json()
    property_id = data.get('property_id')
    offer_amount = data.get('offer_amount')
    client_id = get_jwt_identity()

    prop = Property.query.get(property_id)
    if not prop:
        return jsonify({"msg": "Property not found"}), 404

    # Ensure the user initiating is a client
    user = User.query.get(client_id)
    if user.role.name != 'client':
        return jsonify({"msg": "Only clients can initiate deals"}), 403

    new_deal = Deal(
        property_id=property_id,
        broker_id=prop.broker_id,
        client_id=client_id,
        offer_amount=offer_amount,
        status='initiated'
    )
    db.session.add(new_deal)
    db.session.commit()
    return jsonify({"msg": "Deal initiated", "id": new_deal.id}), 201

@deals_bp.route('/', methods=['GET'])
@jwt_required()
def get_deals():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if user.role.name == 'admin':
        deals = Deal.query.all()
    else:
        # Clients and brokers can see their deals
        deals = Deal.query.filter(
            (Deal.broker_id == current_user_id) | (Deal.client_id == current_user_id)
        ).all()

    return jsonify([d.to_dict() for d in deals]), 200

@deals_bp.route('/<uuid:deal_id>', methods=['PUT'])
@jwt_required()
def update_deal_status(deal_id):
    deal = Deal.query.get(deal_id)
    if not deal:
        return jsonify({"msg": "Deal not found"}), 404

    current_user_id = get_jwt_identity()
    if deal.broker_id != current_user_id and deal.client_id != current_user_id:
        return jsonify({"msg": "Unauthorized"}), 403

    data = request.get_json()

    # Logic for updating status (e.g., countering, accepting)
    # This can be complex depending on the business rules
    if 'status' in data:
        deal.status = data['status']
    if 'offer_amount' in data: # For counter-offers
        deal.offer_amount = data['offer_amount']
    if 'contract_url' in data:
        deal.contract_url = data['contract_url']

    db.session.commit()
    return jsonify({"msg": "Deal updated"}), 200