from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel
from .. import db
import enum

class LeadStatusEnum(enum.Enum):
    new = "new"
    contacted = "contacted"
    negotiating = "negotiating"
    closed = "closed"
    lost = "lost"

class Lead(BaseModel):
    __tablename__ = 'leads'
    client_id = Column(ForeignKey('users.id'), nullable=False)
    client = relationship("User")
    property_id = Column(ForeignKey('properties.id'), nullable=False)
    property = relationship("Property")
    status = Column(db.Enum(LeadStatusEnum), default=LeadStatusEnum.new)

    def to_dict(self):
        return {
            "id": str(self.id),
            "client_id": str(self.client_id),
            "property_id": str(self.property_id),
            "status": self.status.name,
            "created_at": self.created_at.isoformat()
        }