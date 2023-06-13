from datetime import datetime

from mongoengine import StringField, DateField, BooleanField
from pydantic import BaseModel


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
