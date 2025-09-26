from sqlalchemy import Column, String, ForeignKey, JSON
from sqlalchemy.orm import relationship
from .base import BaseModel

class Message(BaseModel):
    __tablename__ = 'messages'
    conversation_id = Column(ForeignKey('conversations.id'), nullable=False)
    conversation = relationship("Conversation")
    sender_id = Column(ForeignKey('users.id'), nullable=False)
    sender = relationship("User", foreign_keys=[sender_id])
    receiver_id = Column(ForeignKey('users.id'), nullable=False)
    receiver = relationship("User", foreign_keys=[receiver_id])
    body = Column(String, nullable=False)
    attachments = Column(JSON, nullable=True) # Array of URLs

    def to_dict(self):
        return {
            "id": str(self.id),
            "conversation_id": str(self.conversation_id),
            "sender_id": str(self.sender_id),
            "receiver_id": str(self.receiver_id),
            "body": self.body,
            "attachments": self.attachments,
            "created_at": self.created_at.isoformat()
        }