from pydantic import BaseModel


class JWTLoginSchema(BaseModel):
	username: str
	password: str


class JWTRegisterSchema(JWTLoginSchema):
	email: str
	re_password: str