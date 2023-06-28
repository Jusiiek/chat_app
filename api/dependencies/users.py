from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from jose import JWTError, jwt

from config.enviroments import SECRET_KEY, SECRET_ALGORITHM
from models.users import User
from config.db_config import get_sql_db


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
# in minutes
TOKEN_LIFE_TIME = 60 * 24


def get_user(user_name: str, db: Depends(get_sql_db)):
    if user_name:
        user = db.query(User).filter(User.username == user_name).first()
        if user:
            return user
        else:
            return None
    return None


def authenticate_user(user_name: str, password: str, db):
    user = get_user(user_name, db)
    if not user:
        return False
    if user and user.password != password:
        return False
    return user


def create_access_token(data: dict):
    to_encode = data.copy()

    expire_date = datetime.today() + timedelta(minutes=TOKEN_LIFE_TIME)
    to_encode.update({"exp": expire_date})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=SECRET_ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)],
                           db: Depends(get_sql_db)):
    credentials_exception = HTTPException(
        status=status.HTTP_401_UNAUTHORIZED,
        detail="Could not valid credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    username = ''
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[SECRET_ALGORITHM])
        username = payload.get('sub')
        if not username:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = get_user(db, username)
    if user is None:
        raise credentials_exception
    return user
