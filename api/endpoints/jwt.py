from fastapi import APIRouter, Depends

from app import session_db
from scheme.users import UserLoginSchema, UserRegisterSchema


router = APIRouter(
	prefix="/api/jwt",
	tags=['jwt']
)


@router.post("/login/")
def jwt_login(payload: UserLoginSchema, db: Depends(session_db)):
	pass


@router.post("/register/")
def jwt_register(payload: UserRegisterSchema, db:Depends(session_db)):
	pass