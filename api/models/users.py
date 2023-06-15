from datetime import datetime

from mongoengine import StringField, DateField, BooleanField
from pydantic import BaseModel, validator


class User(BaseModel):
	email = StringField(required=True, unique=True, max_length=70)
	username = StringField(required=True, unique=True, max_length=70)
	password = StringField(max_length=100)
	created_at = DateField(default=datetime.now())
	updated_at = DateField(default=datetime.now())
	last_logged = DateField(default=datetime.now())
	role = StringField(max_length=100)
	is_active = BooleanField(default=False)
	banned = BooleanField(default=False)

	@validator("password")
	def valid_password(self, p: str):
		if p and len(p) < 8:
			raise ValueError("Password should be at least 8 characters")
		return p
