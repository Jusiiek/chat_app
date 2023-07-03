import click
import asyncio
from functools import wraps

from config.db_config import mysql_engine
from models import Base
from utils import inject_data_from_excel


def coroutine(f):
	@wraps(f)
	def wrapper(*args, **kwargs):
		return asyncio.get_event_loop().run_until_complete(f(*args, **kwargs))
	
	return wrapper


@click.group()
def cli():
	"""Management script."""


@cli.command('mariadb-setup-tables')
async def setup_mariadb():
	def get_tables():
		from models import Role
		from models import User
		from models import Ban

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


@cli.command('database-load-fixtures')
@click.option('-c', '--chat-app-data', is_flag=True, help="Injection data from fixtures")
async def injection_fixtures(chat_app_data):
	if chat_app_data:
		await inject_data_from_excel("fixtures.xlsx")
		click.echo("Injected fixtures from excel")


if __name__ == '__name__':
	print("STARTING")
	cli()