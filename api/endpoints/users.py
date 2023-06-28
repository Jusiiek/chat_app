from fastapi import APIRouter, Depends

from typing import Annotated

from dependencies.users import get_current_user
from models.users import User


router = APIRouter(
	prefix="/api/user",
	tags=['users'],
)


@router.get("/")
def get_users(user: Depends(get_current_user)):
	print("User", user)
