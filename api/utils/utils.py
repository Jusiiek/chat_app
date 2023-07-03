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

		dates_columns = [
			"created_at",
			"updated_at",
			"last_logged",
			"ban_expire"
		]

		for index, sheet in enumerate(sheet_names):

			print(f"\n\t Handling table {sheet} {(index+1) / {len(sheet_names)}}")
			print("\t\t Reading data...")

			df = data_file.parse(sheet)
			print(df.columns)
			for col in list(df.columns):
				if col in dates_columns:
					df[col] = pd.to_datetime(df[col])
					if df[col] in ["created_at"]:
						df[col].fillna(value=date_now, inplace=True)

			print(f"Injecting data {df.shape[0]} rows")
			df.to_sql(
				sheet,
				db.bind,
				if_exists="append",
				index=False
			)
			print("\t Done")
		db.commit()
