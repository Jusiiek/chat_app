from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status

from dependencies.users import get_current_user
from scheme.users import UserCreateSchema, UserUpdateSchema

from utils.auth_utils import (
	valid_password,
	valid_user_in_db,
	create_hash_password,
	get_user_by_username,
	get_user_by_email
)
from utils import get_role_id

from models.cassandra.users import User
from models.cassandra.role import Role

router = APIRouter(
	prefix="/api/users",
	tags=['users'],
	dependencies=[Depends(get_current_user)]
)


@router.get("/")
def get_users():
	users_list = User.objects.all()
	return users_list


router.get("/{user_id}/")
def get_user(user_id: str):
	user = User.objects.filter(user_id=user_id)
	if not user:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="User not found"
		)
	return user.first()


@router.post("/")
def create_user(user: Depends(get_current_user), payload: UserCreateSchema):

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
		role_id=get_role_id(payload.role_name),
		created_by=user.user_id,
		updated_by=user.user_id
	)
	new_user.save()

	return new_user


@router.put("/{user_id}/")
def update_user(
	user_id: str,
	user: Depends(get_current_user),
	payload: UserUpdateSchema
):
	payload = payload.dict()

	if payload['password']:
		valid_password_error = valid_password(payload['password'])
		if valid_password_error:
			raise HTTPException(
				status_code=status.HTTP_400_BAD_REQUEST,
				detail=f"{valid_password_error}",
			)

	if payload['username']:
		user = get_user_by_username(payload['username'])
		if user:
			raise HTTPException(
				status_code=status.HTTP_400_BAD_REQUEST,
				detail="Username already taken"
			)

	if payload['email']:
		user = get_user_by_email(payload['email'])
		if user:
			raise HTTPException(
				status_code=status.HTTP_400_BAD_REQUEST,
				detail="Email already taken"
			)

	if payload['role_name']:
		role_name = payload.pop('role_name')

	user_to_update = User.objects.filter(user_id=user_id)
	if user_to_update:
		user_to_update = user_to_update.first()

		user_to_update.update(
			**payload,
			role_id=get_role_id(role_name),
			updated_at=datetime.now(),
			updated_by=user.user_id
		)
		if role_name == Role.ROLE_ADMIN:
			user_to_update.update(
				is_admin=True
			)
		else:
			user_to_update.update(
				is_admin=False
			)

		user_to_update.save()

		return user_to_update
	else:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="User not found"
		)


@router.delete("/{user_id}/")
def delete_user(user_id: str):
	user_delete = User.objects.filter(user_id=user_id)
	if not user_delete:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="User not found"
		)
	user_delete.first().delete()

	return {}
