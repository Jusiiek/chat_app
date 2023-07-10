from pydantic import BaseModel


class UserCreateSchema(BaseModel):
	email: str
	username: str
	password: str
	created_by: str
	role_name: str
