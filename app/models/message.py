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