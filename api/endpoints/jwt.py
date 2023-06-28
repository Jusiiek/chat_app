from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status

from config.db_config import get_sql_db

from models.users import User
from scheme.users import UserLoginSchema, UserRegisterSchema
from dependencies.users import authenticate_user, create_access_token


router = APIRouter(
	prefix="/api/jwt",
	tags=['jwt']
)


@router.get("/test/")
def jwt_login(db=Depends(get_sql_db)):
	user = db.query(User).all()
	print(user)
	return {
		"Connected": "HELLO"
	}


@router.post("/login/")
def jwt_login(login_data: UserLoginSchema):
	user = authenticate_user(login_data['username'], login_data['password'])
	if not user:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Incorrect username or password",
			headers={"WWW-Authenticate": "Bearer"},
		)

	access_token = create_access_token(data={"sub": user.username})
	return {"access_token": access_token,
		"user_data": user,
		"token_type": "bearer"
	}


@router.post("/register/")
def jwt_register(payload: UserRegisterSchema, db=Depends(get_sql_db)):
	print(payload)

	passw = payload.password
	re_passw = payload.re_password


	print("==========================", passw)
	if passw != re_passw:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail="Passwords don't match",
		)

	print("AFTER PASS COMPARE")
	existed_user = authenticate_user(payload.username, passw, db)
	if existed_user:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail="Username already in use",
		)

	check_email = db.query(User).get(email=payload.email)
	if check_email:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail="Email already in use",
		)

	new_user = User(
		**payload,
		created_at=datetime.now(),
		updated_at=datetime.now(),
		last_logged=datetime.now(),
		role='User',
		is_active=False,
		banned=False,
	)

	db.add(new_user)
	db.commit()
	return new_user
