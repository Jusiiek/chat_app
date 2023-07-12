from datetime import datetime

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

from scheme.jwt import JWTLoginSchema, JWTRegisterSchema
from dependencies.users import authenticate_user, create_token
from utils.auth_utils import (
	valid_user_in_db,
	valid_password,
	create_hash_password,
	check_if_user_is_active,
	check_if_user_has_a_ban
)

from utils import get_role_id

from models.cassandra.users import User
from models.cassandra.role import Role

router = APIRouter(
	prefix="/api/jwt",
	tags=['jwt']
)


@router.post("/login/")
async def jwt_login(payload: JWTLoginSchema):
	user = authenticate_user(payload.username, payload.password)
	if not user:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Incorrect username or password",
		)

	active_message = await check_if_user_is_active(user)
	if active_message:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail=active_message,
		)

	ban_type, ban = await check_if_user_has_a_ban(user)
	if ban_type and ban:
		return JSONResponse(
			status_code=401,
			content={
				"main_message": f"Your account has been {ban_type} banned",
				"ban": ban
			}
		)

	access_token = create_token(data={"user": user.username})
	user.last_logged = datetime.now()
	user.save()

	role = Role.objects.get(role_id=user.role_id)

	return {
		"token": access_token,
		"token_type": "Bearer",
		"user_data": user,
		"role_data": role
	}


@router.post("/register/")
def jwt_register(payload: JWTRegisterSchema):
	if payload.password != payload.re_password:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail="Passwords don't match",
		)

	valid_password_error = valid_password(payload.password)
	if valid_password_error:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail=f"{valid_password_error}",
		)

	valid_user_errors = valid_user_in_db(
		payload.email, payload.username
	)

	if valid_user_errors:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail=f"{valid_user_errors['error']} already in use",
		)

	new_user = User.create(
		email=payload.email,
		username=payload.username,
		password=create_hash_password(payload.password),
		role_id=get_role_id(Role.ROLE_USER)
	)
	new_user.save()

	return new_user
