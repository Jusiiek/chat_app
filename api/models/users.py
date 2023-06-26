from datetime import datetime

from pydantic import BaseModel, validator


class User(BaseModel):
	email: str
	username: str
	password: str
	created_at: datetime
	updated_at: datetime
	last_logged: datetime
	role: str
	is_active: bool
	banned: bool

	@validator("password")
	def valid_password(cls, p: str):
		if p and len(p) < 8:
			raise ValueError("Password should be at least 8 characters")
		return p
