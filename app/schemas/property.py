from .. import ma
from ..models import Property
from marshmallow import fields

class PropertySchema(ma.SQLAlchemyAutoSchema):
    property_type = fields.String(attribute="property_type.name")
    status = fields.String(attribute="status.name")

    class Meta:
        model = Property
        load_instance = True
        include_fk = True

property_schema = PropertySchema()
properties_schema = PropertySchema(many=True)