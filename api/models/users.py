from datetime import datetime

from sqlalchemy import Column, ForeignKey, String, DateTime, Boolean, text
from sqlalchemy.dialects.mysql import INTEGER

from models import Base

class User(Base):
    __tablename__ = "Users"

    user_id = Column(INTEGER(unsigned=True), primary_key=True, nullable=False, autoincrement=True)
    email = Column(String(100), nullable=False, unique=True)
    username = Column(String(100), nullable=False, unique=True)
    password = Column(String(200), nullable=False)
    created_at = Column(
        DateTime, default=datetime.now, server_default=text("NOW()"), nullable=False
    )
    updated_at = Column(
        DateTime, default=datetime.now, server_default=text("NOW()"), nullable=False
    )
    last_logged = Column(
        DateTime, default=datetime.now, server_default=text("NOW()"), nullable=False
    )
    role_id = Column(
        ForeignKey("Role.role_id", ondelete="CASCADE"), nullable=False, default=5
    )
    is_active = Column(Boolean, default=False)
    banned = Column(Boolean, default=False)
