import json

from models.cassandra.role import Role

ADMIN_ROLES = ["SUPER_ADMIN", "ADMIN"]


def is_user_super_user(role):
	return role == "SUPER_ADMIN"


def is_user_admin(role):
	return any(role in ADMIN_ROLES)


def get_role_id(role_name: str):
	return Role.objects.get(name=role_name).role_id


def read_json(file_path: str) -> dict:
	if not file_path.is_file():
		return {}

	try:
		with file_path.open("r") as rf:
			return json.load(rf)
	except (json.JSONDecoder, FileNotFoundError):
		print("Couldn't find json file. 😢")
		return {}
