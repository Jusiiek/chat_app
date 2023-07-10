from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from jose import jwt, JWTError

from config.enviroments import SECRET_KEY, SECRET_ALGORITHM
from utils.auth_utils import (
    get_user_by_username,
    verify_password
)
from models.cassandra.users import User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
# in minutes
TOKEN_LIFE_TIME = 60 * 24


def authenticate_user(username: str, password: str):
    user = get_user_by_username(username)
    if user:
        return user \
            if verify_password(password, user.password) \
            else None
    else:
        return None


def create_token(data: dict):
    to_encode = data.copy()
    expire_time = datetime.now() + timedelta(TOKEN_LIFE_TIME)
    to_encode.update({"exp": expire_time})
    encoded_jwt = jwt.encode(
        to_encode, SECRET_KEY, algorithm=SECRET_ALGORITHM
    )
    return encoded_jwt


def get_current_user_by_token(token: str = Depends(oauth2_scheme)) -> User:
    http_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.encode(token, SECRET_KEY, algorithm=SECRET_ALGORITHM)
        username = payload['user']
    except JWTError:
        raise http_exception

    user = get_user_by_username(username)
    return user


def get_current_user(current_user: User = Depends(get_current_user_by_token)) -> User:
    return current_user
