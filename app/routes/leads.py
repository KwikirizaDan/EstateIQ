from flask import request, jsonify, Blueprint
from .. import db
from ..models import Lead, User, Property
from flask_jwt_extended import jwt_required, get_jwt_identity

leads_bp = Blueprint('leads', __name__, url_prefix='/leads')

@leads_bp.route('/', methods=['POST'])
@jwt_required()
def create_lead():
    data = request.get_json()
    property_id = data.get('property_id')
    current_user_id = get_jwt_identity()

    user = User.query.get(current_user_id)
    if not user or user.role.name != 'client':
        return jsonify({"msg": "Only clients can create leads"}), 403

    if not Property.query.get(property_id):
        return jsonify({"msg": "Property not found"}), 404

    new_lead = Lead(
        client_id=current_user_id,
        property_id=property_id,
        status='new'
    )
    db.session.add(new_lead)
    db.session.commit()
    return jsonify({"msg": "Lead created", "id": new_lead.id}), 201

@leads_bp.route('/', methods=['GET'])
@jwt_required()
def get_leads():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if user.role.name == 'broker':
        # A broker might see all leads for their properties
        leads = Lead.query.join(Property).filter(Property.broker_id == current_user_id).all()
    elif user.role.name == 'client':
        leads = Lead.query.filter_by(client_id=current_user_id).all()
    else: # Admin
        leads = Lead.query.all()

    return jsonify([l.to_dict() for l in leads]), 200

@leads_bp.route('/<uuid:lead_id>', methods=['PUT'])
@jwt_required()
def update_lead_status(lead_id):
    lead = Lead.query.get(lead_id)
    if not lead:
        return jsonify({"msg": "Lead not found"}), 404

    # Authorization: only broker associated with the property can update
    prop = Property.query.get(lead.property_id)
    current_user_id = get_jwt_identity()
    if prop.broker_id != current_user_id:
        return jsonify({"msg": "Unauthorized"}), 403

    data = request.get_json()
    new_status = data.get('status')
    if new_status:
        lead.status = new_status
        db.session.commit()
        return jsonify({"msg": "Lead status updated"}), 200

    return jsonify({"msg": "Missing status"}), 400