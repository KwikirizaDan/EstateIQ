from sqlalchemy import Column, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel
from .. import db
import enum

class PropertyTypeEnum(enum.Enum):
    land = "land"
    house = "house"
    rental = "rental"

class PropertyStatusEnum(enum.Enum):
    available = "available"
    under_offer = "under_offer"
    sold = "sold"
    rented = "rented"

class Property(BaseModel):
    __tablename__ = 'properties'
    title = Column(String(255), nullable=False)
    description = Column(String, nullable=True)
    property_type = Column(db.Enum(PropertyTypeEnum), name="type", nullable=False)
    address = Column(String(255), nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    price = Column(Float, nullable=False)
    size = Column(Float, nullable=False)
    size_unit = Column(String(20), nullable=False) # acres, square feet
    status = Column(db.Enum(PropertyStatusEnum), nullable=False, default=PropertyStatusEnum.available)
    broker_id = Column(ForeignKey('users.id'), nullable=False)
    broker = relationship("User")