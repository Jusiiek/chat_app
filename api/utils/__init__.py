import json
from pathlib import Path

ADMIN_ROLES = ["SUPER_ADMIN", "ADMIN"]


def is_user_super_user(role):
	return role == "SUPER_ADMIN"


def is_user_admin(role):
	return any(role in ADMIN_ROLES)


def read_json(file_path: Path) -> dict:
	if not file_path.is_file():
		return {}

	try:
		with file_path.open("r") as rf:
			return json.load(rf)
	except (json.JSONDecoder, FileNotFoundError):
		return {}
