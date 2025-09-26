from flask import request, jsonify, Blueprint
from .. import db
from ..models import Listing, Property
from flask_jwt_extended import jwt_required, get_jwt_identity
import datetime

listings_bp = Blueprint('listings', __name__, url_prefix='/listings')

@listings_bp.route('/', methods=['POST'])
@jwt_required()
def create_listing():
    data = request.get_json()
    property_id = data.get('property_id')

    prop = Property.query.get(property_id)
    if not prop:
        return jsonify({"msg": "Property not found"}), 404

    current_user_id = get_jwt_identity()
    if prop.broker_id != current_user_id:
        return jsonify({"msg": "Only the property broker can create a listing"}), 403

    new_listing = Listing(
        property_id=property_id,
        visibility=data.get('visibility', 'private'),
        media_urls=data.get('media_urls'),
        published_at=datetime.datetime.utcnow() if data.get('visibility') == 'public' else None
    )
    db.session.add(new_listing)
    db.session.commit()
    return jsonify({"msg": "Listing created", "id": new_listing.id}), 201

@listings_bp.route('/', methods=['GET'])
def get_listings():
    listings = Listing.query.filter_by(visibility='public').all()
    return jsonify([l.to_dict() for l in listings]), 200

@listings_bp.route('/<uuid:listing_id>', methods=['GET'])
def get_listing(listing_id):
    listing = Listing.query.get(listing_id)
    if not listing or listing.visibility != 'public':
        # You might want to allow brokers to see private listings
        return jsonify({"msg": "Listing not found or is private"}), 404
    return jsonify(listing.to_dict()), 200

@listings_bp.route('/<uuid:listing_id>', methods=['PUT'])
@jwt_required()
def update_listing(listing_id):
    listing = Listing.query.get(listing_id)
    if not listing:
        return jsonify({"msg": "Listing not found"}), 404

    prop = Property.query.get(listing.property_id)
    current_user_id = get_jwt_identity()
    if prop.broker_id != current_user_id:
        return jsonify({"msg": "Unauthorized"}), 403

    data = request.get_json()

    # Update visibility and published_at
    if 'visibility' in data and data['visibility'] != listing.visibility.name:
        listing.visibility = data['visibility']
        if data['visibility'] == 'public':
            listing.published_at = datetime.datetime.utcnow()
        else:
            listing.published_at = None # Or keep the date, depending on requirements

    if 'media_urls' in data:
        listing.media_urls = data['media_urls']

    db.session.commit()
    return jsonify({"msg": "Listing updated"}), 200

@listings_bp.route('/<uuid:listing_id>', methods=['DELETE'])
@jwt_required()
def delete_listing(listing_id):
    listing = Listing.query.get(listing_id)
    if not listing:
        return jsonify({"msg": "Listing not found"}), 404

    prop = Property.query.get(listing.property_id)
    current_user_id = get_jwt_identity()
    if prop.broker_id != current_user_id:
        return jsonify({"msg": "Unauthorized"}), 403

    db.session.delete(listing)
    db.session.commit()
    return jsonify({"msg": "Listing deleted"}), 200