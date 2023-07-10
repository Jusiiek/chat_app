from pydantic import BaseModel


class JWTLoginSchema(BaseModel):
	username: str
	password: str


class JWTRegisterSchema(BaseModel):
	email: str
	username: str
	password: str
	re_password: str