from datetime import datetime

from pydantic import BaseModel
from mongoengine import StringField, DateField


class Ban(BaseModel):
	username = StringField(max_length=70)
	reason = StringField(max_length=500)
	ban_expire = DateField(default=datetime.now())
	ban_expire_str = StringField(max_length=50)