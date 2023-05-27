from datetime import date

from pydantic import BaseModel

from models.roel import Role


class User(BaseModel):
	email: str
	username: str
	password: str
	created_at: date
	updated_at: date
	last_logged: date
	role: Role
	is_banned: bool
