from pydantic import BaseModel


class UserLoginSchema(BaseModel):
	username: str
	password: str


class UserRegisterSchema(BaseModel):
	email: str
	username: str
	password: str
	re_password: str
