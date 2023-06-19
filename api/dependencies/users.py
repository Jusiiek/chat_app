from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from jose import JWTError, jwt

from api.config.enviroments import SECRET_KEY, SECRET_ALGORITHM
from api.config.mongo_config import get_db_client
from api.models.users import User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
# in seconds
TOKEN_LIFE_TIME = 60 * 60 * 24


def get_user(db, username):
	if username:
		user = db.query(User).get(username)
		return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status=status.HTTP_401_UNAUTHORIZED,
        detail="Could not valid credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    username: str = ''
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[SECRET_ALGORITHM])
        username = payload.get('sub')
        if username is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = get_user(get_db_client, username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
