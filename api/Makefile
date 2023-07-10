dev_install_requirements:
	@pip install -r ./requirements.txt

dev_run:
	@python app.py

check_code:
	@flake8 .

db_setup_and_load_fixtures:
	@python cli.py cassandra-setup
	@python cli.py database-load-fixtures -c
