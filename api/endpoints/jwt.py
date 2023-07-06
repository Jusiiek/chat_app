from fastapi import APIRouter, HTTPException, status

from scheme.users import UserLoginSchema, UserRegisterSchema
from dependencies.users import authenticate_user, create_token
from utils.auth_utils import valid_user_in_db, valid_password

from models.cassandra.users import User

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
	access_token = create_token(data={"user": user.username})
	return {
		"token": access_token,
		"token_type": "bearer",
		"user_data": user
	}


@router.post("/register/")
def jwt_register(payload: UserRegisterSchema):
	if payload['password'] != payload['re_password']:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail="Passwords don't match",
			headers={"WWW-Authenticate": "Bearer"},
		)

	valid_password_error = valid_password(payload['password'])
	if valid_password_error:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail=f"{valid_password_error} already in use",
			headers={"WWW-Authenticate": "Bearer"},
		)

	valid_user_errors = valid_user_in_db(
		payload['email'], payload['username']
	)

	if valid_user_errors:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail=f"{valid_user_errors['error']} already in use",
			headers={"WWW-Authenticate": "Bearer"},
		)

	new_user = User.create(
		**payload,
		role_id=5
	)

	return new_user