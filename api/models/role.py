from sqlalchemy import Column, String
from sqlalchemy.dialects.mysql import INTEGER

from models import Base


class Role(Base):
	__tablename__ = "Roles"

	role_id = Column(INTEGER(unsigned=True), primary_key=True, nullable=False, autoincrement=True)
	name = Column(String(20), nullable=False)
	pseudo_name = Column(String(20), nullable=False)
