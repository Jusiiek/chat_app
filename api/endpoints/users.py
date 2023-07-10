from fastapi import APIRouter, Depends

from dependencies.users import get_current_user

from models.cassandra.users import User

router = APIRouter(
	prefix="/api/user",
	tags=['users'],
	dependencies=[Depends(get_current_user)]
)


@router.get("/")
def get_users():
	users_list = User.objects.all()
	return users_list


@router.delete("/{user_id}/")
def delete_user(user_id: str):
	user_delete = User.objects.filter(user_id=user_id).first()
	user_delete.delete()

	return {}
