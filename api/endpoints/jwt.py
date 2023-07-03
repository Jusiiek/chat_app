from fastapi import APIRouter, HTTPException, status

from scheme.users import UserLoginSchema, UserRegisterSchema
from dependencies.users import authenticate_user


router = APIRouter(
	prefix="/api/jwt",
	tags=['jwt']
)


@router.post("/login/")
def jwt_login(login_data: UserLoginSchema):
	user = authenticate_user(login_data['username'], login_data['password'])
	if not user:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Incorrect username or password",
			headers={"WWW-Authenticate": "Bearer"},
		)


@router.post("/register/")
def jwt_register(payload: UserRegisterSchema):
	pass
