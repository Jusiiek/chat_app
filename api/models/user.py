from datetime import date

from pydantic import BaseModel


class Role(BaseModel):
	name: str
	pseudo_name: str


class User(BaseModel):
	email: str
	username: str
	password: str
	created_at: date
	updated_at: date
	last_logged: date
	role: Role
	is_banned: bool
