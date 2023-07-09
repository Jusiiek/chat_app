from datetime import datetime
from pathlib import Path

import pandas as pd
from cassandra.cqlengine.management import (
	sync_table,
	drop_table,
)

from config.db_config import get_sql_db

from utils import read_json
from utils.auth_utils import create_hash_password

from models.cassandra.role import Role
from models.cassandra.users import User
from models.cassandra.ban import Ban


async def get_cassandra_models():
	return (
		Role,
		User,
		Ban
	)


async def drop_all_cassandra_tables():
	print("DROPPING ALL TABLES FOR CASSANDRA")
	cassandra_models = await get_cassandra_models()
	for model in cassandra_models:
		drop_table(model)
		print(f"Dropped {model.__name__}s table")


async def create_cassandra_tables():
	print("CREATING ALL TABLES FOR CASSANDRA")
	cassandra_models = await get_cassandra_models()
	for model in cassandra_models:
		sync_table(model)
		print(f"CREATED {model.__name__}s table")


async def inject_model_data(model, file: str):
	print(f"INJECTING DATA FOR {model.__name__}s")
	file_path = Path(__file__).parent.parent.resolve() / f"fixtures/{file}"
	model_data = read_json(file_path)

	if model_data:
		if model.__name__ == "User":
			for data in model_data:
				user_pass = data.pop('password')
				new_model = model.create(
					**data,
					password=create_hash_password(user_pass)
				)
				new_model.save()
		else:
			for data in model_data:
				new_model = model.create(
					**data,
				)
				new_model.save()

		print(f"Created {len(model_data)} {model.__name__}s")


async def inject_json_data():
	await inject_model_data(Role, "role.json")
	await inject_model_data(User, "users.json")


async def inject_data_from_excel(file: str):
	db = next(get_sql_db())
	date_now = datetime.now()

	try:
		data_path = Path(__file__).parent.parent.resolve() / f"fixtures/{file}"
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
