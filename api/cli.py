import click


@click.group()
def cli():
	"""Management script."""


@cli.command('database-fixtures')
@click.option('-u', '--users', is_flag=True, help="Injection users fixtures")
@click.option('-r', '--roles', is_flag=True, help="Injection roles fixtures")
async def injection_fixtures(users, roles):
	if users:
		pass
	if roles:
		pass
