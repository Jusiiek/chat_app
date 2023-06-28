from datetime import datetime

from sqlalchemy import Column, ForeignKey, String, DateTime, text
from sqlalchemy.dialects.mysql import INTEGER

from models import Base


class Ban(Base):
	__tablename__ = "Bans"

	ban_id = Column(INTEGER(unsigned=True), primary_key=True, nullable=False, autoincrement=True)
	user_id = Column(ForeignKey("User.user_id", ondelete="CASCADE"), nullable=False)
	reason = Column(String(300), nullable=False)
	ban_expire_str = Column(String(10), nullable=False)
