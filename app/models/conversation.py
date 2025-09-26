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

    def to_dict(self):
        return {
            "id": str(self.id),
            "deal_id": str(self.deal_id) if self.deal_id else None,
            "property_id": str(self.property_id) if self.property_id else None,
            "participants": self.participants,
            "created_at": self.created_at.isoformat()
        }