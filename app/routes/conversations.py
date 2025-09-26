from flask import request, jsonify, Blueprint
from .. import db
from ..models import Conversation, Deal, Property, User
from ..schemas import conversation_schema, conversations_schema
from flask_jwt_extended import jwt_required, get_jwt_identity

conversations_bp = Blueprint('conversations', __name__, url_prefix='/conversations')

@conversations_bp.route('/', methods=['POST'])
@jwt_required()
def create_conversation():
    data = request.get_json()
    deal_id = data.get('deal_id')
    property_id = data.get('property_id')

    participants = []

    if deal_id:
        deal = Deal.query.get(deal_id)
        if not deal:
            return jsonify({"msg": "Deal not found"}), 404
        participants = [str(deal.broker_id), str(deal.client_id)]
    elif property_id:
        prop = Property.query.get(property_id)
        if not prop:
            return jsonify({"msg": "Property not found"}), 404
        participants = [str(prop.broker_id), str(get_jwt_identity())]
    else:
        return jsonify({"msg": "deal_id or property_id is required"}), 400

    new_conversation = Conversation(
        deal_id=deal_id,
        property_id=property_id,
        participants=participants
    )
    db.session.add(new_conversation)
    db.session.commit()
    return jsonify(conversation_schema.dump(new_conversation)), 201

@conversations_bp.route('/', methods=['GET'])
@jwt_required()
def get_conversations():
    current_user_id = get_jwt_identity()
    conversations = Conversation.query.filter(Conversation.participants.contains(current_user_id)).all()
    return jsonify(conversations_schema.dump(conversations)), 200