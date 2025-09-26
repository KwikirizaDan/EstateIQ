from flask import request, jsonify, Blueprint
from .. import db
from ..models import Property, User
from ..schemas import property_schema, properties_schema
from flask_jwt_extended import jwt_required, get_jwt_identity

properties_bp = Blueprint('properties', __name__, url_prefix='/properties')

@properties_bp.route('/', methods=['POST'])
@jwt_required()
def create_property():
    data = request.get_json()
    current_user_id = get_jwt_identity()

    user = User.query.get(current_user_id)
    if not user or user.role.name != 'broker':
        return jsonify({"msg": "Only brokers can create properties"}), 403

    new_property = Property(
        title=data.get('title'),
        description=data.get('description'),
        property_type=data.get('type'),
        address=data.get('location', {}).get('address'),
        latitude=data.get('location', {}).get('latitude'),
        longitude=data.get('location', {}).get('longitude'),
        price=data.get('price'),
        size=data.get('size', {}).get('value'),
        size_unit=data.get('size', {}).get('unit'),
        broker_id=current_user_id
    )
    db.session.add(new_property)
    db.session.commit()
    return jsonify(property_schema.dump(new_property)), 201

@properties_bp.route('/', methods=['GET'])
def get_properties():
    properties = Property.query.all()
    return jsonify(properties_schema.dump(properties)), 200

@properties_bp.route('/<uuid:property_id>', methods=['GET'])
def get_property(property_id):
    prop = Property.query.get(property_id)
    if not prop:
        return jsonify({"msg": "Property not found"}), 404
    return jsonify(property_schema.dump(prop)), 200

@properties_bp.route('/<uuid:property_id>', methods=['PUT'])
@jwt_required()
def update_property(property_id):
    prop = Property.query.get(property_id)
    if not prop:
        return jsonify({"msg": "Property not found"}), 404

    current_user_id = get_jwt_identity()
    if str(prop.broker_id) != current_user_id:
        return jsonify({"msg": "Unauthorized"}), 403

    data = request.get_json()
    for key, value in data.items():
        if hasattr(prop, key):
            setattr(prop, key, value)

    db.session.commit()
    return jsonify(property_schema.dump(prop)), 200

@properties_bp.route('/<uuid:property_id>', methods=['DELETE'])
@jwt_required()
def delete_property(property_id):
    prop = Property.query.get(property_id)
    if not prop:
        return jsonify({"msg": "Property not found"}), 404

    current_user_id = get_jwt_identity()
    if str(prop.broker_id) != current_user_id:
        return jsonify({"msg": "Unauthorized"}), 403

    db.session.delete(prop)
    db.session.commit()
    return jsonify({"msg": "Property deleted"}), 200