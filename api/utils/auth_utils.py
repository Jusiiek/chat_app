from passlib.context import CryptContext

from models.cassandra.users import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hash_password: str):
	pwd_context.verify(plain_password, hash_password)


def get_has_password(password: str):
	pwd_context.hash(password)


def get_user(username: str):
	if username:
		user = User.filter(username=username)
		return user.first() if user else None
