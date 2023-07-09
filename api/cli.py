import click
import asyncio
from functools import wraps

# from models.sql import Base
from config.db_config import (
	cassandra_connect,
	cassandra_close
)
from utils.fixture_utils import (
	inject_data_from_excel,
	inject_json_data,
	drop_all_cassandra_tables,
	create_cassandra_tables
)


def coroutine(f):
	@wraps(f)
	def wrapper(*args, **kwargs):
		return asyncio.get_event_loop().run_until_complete(f(*args, **kwargs))

	return wrapper


@click.group()
def cli():
	"""Management script."""


# TODO implement same function for cassandra as below
# @cli.command('mariadb-setup-tables')
# async def setup_mariadb():
# 	def get_tables():
# 		from models import Role
# 		from models import User
# 		from models import Ban
#
# 		return (
# 			Role,
# 			User,
# 			Ban
# 		)
#
# 	get_tables()
# 	Base.metadata.reflect(mysql_engine)
# 	Base.metadata.drop_all(bind=mysql_engine)
# 	Base.metadata.create_all(bind=mysql_engine)
#
# 	click.echo("MariaDB successfully initialized")


@cli.command('cassandra-setup')
@coroutine
async def setup_cassandra():
	print("RUNNING SETUP CASSANDRA")
	cassandra_connect()
	await drop_all_cassandra_tables()
	await create_cassandra_tables()
	cassandra_close()


@cli.command('database-load-fixtures')
@click.option('-c', '--cassandra', is_flag=True, help="Injection data for cassandra")
@click.option('-m', '--mysql', is_flag=True, help="Injection data for mysql")
@coroutine
async def injection_fixtures(cassandra, mysql):
	if cassandra:
		await inject_json_data()
		click.echo("Injected fixtures for cassandra")

	if mysql:
		await inject_data_from_excel("fixtures.xlsx")
		click.echo("Injected fixtures for mysql")


if __name__ == '__main__':
	cli()
