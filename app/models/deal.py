from sqlalchemy import Column, Float, ForeignKey, String
from sqlalchemy.orm import relationship
from .base import BaseModel
from .. import db
import enum

class DealStatusEnum(enum.Enum):
    initiated = "initiated"
    countered = "countered"
    accepted = "accepted"
    rejected = "rejected"
    closed = "closed"

class Deal(BaseModel):
    __tablename__ = 'deals'
    property_id = Column(ForeignKey('properties.id'), nullable=False)
    property = relationship("Property")
    broker_id = Column(ForeignKey('users.id'), nullable=False)
    broker = relationship("User", foreign_keys=[broker_id])
    client_id = Column(ForeignKey('users.id'), nullable=False)
    client = relationship("User", foreign_keys=[client_id])
    offer_amount = Column(Float, nullable=False)
    status = Column(db.Enum(DealStatusEnum), default=DealStatusEnum.initiated)
    contract_url = Column(String(255), nullable=True)

    def to_dict(self):
        return {
            "id": str(self.id),
            "property_id": str(self.property_id),
            "broker_id": str(self.broker_id),
            "client_id": str(self.client_id),
            "offer_amount": self.offer_amount,
            "status": self.status.name,
            "contract_url": self.contract_url,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }