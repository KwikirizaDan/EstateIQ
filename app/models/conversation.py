from sqlalchemy import Column, ForeignKey, JSON
from sqlalchemy.orm import relationship
from .base import BaseModel

class Conversation(BaseModel):
    __tablename__ = 'conversations'
    deal_id = Column(ForeignKey('deals.id'), nullable=True)
    deal = relationship("Deal")
    property_id = Column(ForeignKey('properties.id'), nullable=True)
    property = relationship("Property")
    participants = Column(JSON, nullable=False) # Array of user_ids