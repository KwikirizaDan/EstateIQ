from .. import ma
from ..models import Lead
from marshmallow import fields

class LeadSchema(ma.SQLAlchemyAutoSchema):
    status = fields.String(attribute="status.name")

    class Meta:
        model = Lead
        load_instance = True
        include_fk = True

lead_schema = LeadSchema()
leads_schema = LeadSchema(many=True)