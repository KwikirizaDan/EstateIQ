from .. import ma
from ..models import Listing
from marshmallow import fields

class ListingSchema(ma.SQLAlchemyAutoSchema):
    visibility = fields.String(attribute="visibility.name")

    class Meta:
        model = Listing
        load_instance = True
        include_fk = True

listing_schema = ListingSchema()
listings_schema = ListingSchema(many=True)