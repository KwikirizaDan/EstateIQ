import uuid
from .. import db
from sqlalchemy import Column, DateTime, func
from sqlalchemy.types import UUID

class BaseModel(db.Model):
    __abstract__ = True
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())