import click
import asyncio

from config.db_config import mysql_engine
from models import Base
from utils import inject_data_from_excel

@click.group()
def cli():
	"""Management script."""


@cli.command('mariadb_setup_tables')
async def setup_mariadb():
	def get_tables():
		from models.role import Role
		from models.users import User
		from models.ban import Ban

		return (
			Role,
			User,
			Ban
		)

	get_tables()
	Base.metadata.reflect(mysql_engine)
	Base.metadata.drop_all(bind=mysql_engine)
	Base.metadata.create_all(bind=mysql_engine)

	click.echo("MariaDB successfully initialized")

@cli.command('database-load_fixtures')
@click.option('-cad', '--chat_app_data', is_flag=True, help="Injection users fixtures")
async def injection_fixtures(chat_app_data):
	if chat_app_data:
		await inject_data_from_excel("./fixtures/fixtures.xlsx")
		click.echo("Injected data from excel")
