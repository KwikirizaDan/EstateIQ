from .. import ma
from ..models import Deal
from marshmallow import fields

class DealSchema(ma.SQLAlchemyAutoSchema):
    status = fields.String(attribute="status.name")

    class Meta:
        model = Deal
        load_instance = True
        include_fk = True

deal_schema = DealSchema()
deals_schema = DealSchema(many=True)