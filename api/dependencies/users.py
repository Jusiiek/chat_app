from fastapi.security import OAuth2PasswordBearer

from utils.auth_utils import get_user, verify_password


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
# in minutes
TOKEN_LIFE_TIME = 60 * 24


def authenticate_user(username: str, password: str):
    user = get_user(username)
    return user \
        if user and verify_password(password, user.hashed_password) \
        else None
