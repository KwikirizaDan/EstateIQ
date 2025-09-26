from sqlalchemy import Column, String, Boolean
from .base import BaseModel
from .. import db
import enum

class RoleEnum(enum.Enum):
    broker = "broker"
    client = "client"
    admin = "admin"

class User(BaseModel):
    __tablename__ = 'users'
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(db.Enum(RoleEnum), nullable=False)
    is_verified = Column(Boolean, default=False)