from flask import request, jsonify, Blueprint
from .. import db
from ..models import Message, Conversation, User
from ..schemas import message_schema, messages_schema
from flask_jwt_extended import jwt_required, get_jwt_identity

messages_bp = Blueprint('messages', __name__, url_prefix='/messages')

@messages_bp.route('/', methods=['POST'])
@jwt_required()
def send_message():
    data = request.get_json()
    conversation_id = data.get('conversation_id')
    receiver_id = data.get('receiver_id')
    body = data.get('body')
    sender_id = get_jwt_identity()

    if not all([conversation_id, receiver_id, body]):
        return jsonify({"msg": "Missing required fields"}), 400

    conv = Conversation.query.get(conversation_id)
    if not conv:
        return jsonify({"msg": "Conversation not found"}), 404

    if str(sender_id) not in conv.participants or str(receiver_id) not in conv.participants:
        return jsonify({"msg": "Sender or receiver not in this conversation"}), 403

    new_message = Message(
        conversation_id=conversation_id,
        sender_id=sender_id,
        receiver_id=receiver_id,
        body=body,
        attachments=data.get('attachments')
    )
    db.session.add(new_message)
    db.session.commit()
    return jsonify(message_schema.dump(new_message)), 201

@messages_bp.route('/<uuid:conversation_id>', methods=['GET'])
@jwt_required()
def get_messages(conversation_id):
    current_user_id = get_jwt_identity()

    conv = Conversation.query.get(conversation_id)
    if not conv:
        return jsonify({"msg": "Conversation not found"}), 404

    if str(current_user_id) not in conv.participants:
        return jsonify({"msg": "You are not part of this conversation"}), 403

    messages = Message.query.filter_by(conversation_id=conversation_id).order_by(Message.created_at.asc()).all()
    return jsonify(messages_schema.dump(messages)), 200