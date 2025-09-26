from .. import ma
from ..models import Message

class MessageSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Message
        load_instance = True
        include_fk = True

message_schema = MessageSchema()
messages_schema = MessageSchema(many=True)