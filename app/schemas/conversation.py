from .. import ma
from ..models import Conversation

class ConversationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Conversation
        load_instance = True
        include_fk = True

conversation_schema = ConversationSchema()
conversations_schema = ConversationSchema(many=True)