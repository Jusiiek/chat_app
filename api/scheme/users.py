from pydantic import BaseModel
from typing import Optional


class UserCreateSchema(BaseModel):
	email: str
	username: str
	password: str
	re_password: str
	role_name: str


class UserUpdateSchema(BaseModel):
	email: Optional[str]
	username: Optional[str]
	password: Optional[str]
	role_name: Optional[str]
