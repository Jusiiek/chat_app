from datetime import datetime
from pathlib import Path

import pandas as pd

from config.db_config import get_sql_db

ADMIN_ROLES = ["SUPER_ADMIN", "ADMIN"]


def is_user_super_user(role):
	return role == "SUPER_ADMIN"


def is_user_admin(role):
	return any(role in ADMIN_ROLES)


async def inject_data_from_excel(file: str):
	db = next(get_sql_db())
	date_now = datetime.now()

	try:
		data_path = Path(__file__).parent.resolve() / file
	except Exception as e:
		print(f"Couldn't find file. 😢 {e}")

	if data_path:
		data_file = pd.ExcelFile(data_path)
		sheet_names = data_file.sheet_names

		print(f"Script will now try inject {len(sheet_names)} tables")
