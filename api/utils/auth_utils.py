import re
import string

from passlib.context import CryptContext

from models.cassandra.users import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hash_password: str):
	return pwd_context.verify(plain_password, hash_password)


def create_hash_password(password: str):
	return pwd_context.hash(password)


def get_user_by_username(username: str):
	if username:
		user = User.objects.filter(username=username)
		return user.first() if user else None


def get_user_by_email(email: str):
	if email:
		user = User.objects.filter(email=email)
		return user.first() if user else None


def valid_user_in_db(email: str, username: str):
	if email and username:
		user = get_user_by_email(email)
		if user:
			return {"error": "Email"}
		user = get_user_by_username(username)
		if user:
			return {"error": "User"}


def valid_password(password: str):
	if not re.search(r'[A-Z]', password):
		return "Password must includes at least one uppercase letter"

	if not re.search(r'[a-z]', password):
		return "Password must includes at least one lowercase letter"

	special_chars = string.punctuation
	if not any(char in special_chars for char in password):
		return "Password must includes at least one special character"

	if not re.search(r'[0-9]', password):
		return "Password must includes at least one number"
