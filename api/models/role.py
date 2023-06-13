from pydantic import BaseModel
from mongoengine import StringField


class Role(BaseModel):
	name = StringField(max_length=100)
	pseudo_name = StringField(max_length=100)

