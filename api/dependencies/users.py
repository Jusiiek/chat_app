from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
# in minutes
TOKEN_LIFE_TIME = 60 * 24
