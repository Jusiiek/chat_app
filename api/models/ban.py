from datetime import datetime

from pydantic import BaseModel
from mongoengine import StringField, DateField


class Ban(BaseModel):
	user = StringField(max_length=50)
	reason = StringField(max_length=500)
	ban_expire = DateField(default=datetime.now())
	ban_expire_str = StringField(max_length=50)