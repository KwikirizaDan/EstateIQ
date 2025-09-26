from sqlalchemy import Column, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from .base import BaseModel
from .. import db
import enum

class VisibilityEnum(enum.Enum):
    public = "public"
    private = "private"

class Listing(BaseModel):
    __tablename__ = 'listings'
    property_id = Column(ForeignKey('properties.id'), nullable=False)
    property = relationship("Property")
    published_at = Column(DateTime, nullable=True)
    visibility = Column(db.Enum(VisibilityEnum), default=VisibilityEnum.private)
    media_urls = Column(JSON, nullable=True)

    def to_dict(self):
        return {
            "id": str(self.id),
            "property_id": str(self.property_id),
            "published_at": self.published_at.isoformat() if self.published_at else None,
            "visibility": self.visibility.name,
            "media_urls": self.media_urls,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }