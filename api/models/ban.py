from datetime import datetime

from sqlalchemy import Column, ForeignKey, String, DateTime, text, Boolean
from sqlalchemy.dialects.mysql import INTEGER

from models import Base


class Ban(Base):
	__tablename__ = "Bans"

	ban_id = Column(INTEGER(unsigned=True), primary_key=True, nullable=False, autoincrement=True)
	user_id = Column(ForeignKey("User.user_id", ondelete="CASCADE"), nullable=False)
	reason = Column(String(300), nullable=False)
	created_by = Column(String(100), nullable=False)
	created_at = Column(
		DateTime, default=datetime.now, server_default=text("NOW()"), nullable=False
	)
	ban_expire = Column(
		DateTime, default=datetime.now, server_default=text("NOW()"), nullable=False
	)
	is_permanently_banned = Column(Boolean)
