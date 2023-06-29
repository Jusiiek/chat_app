dev_install_requirements:
	@pip install -r ./requirements.txt

dev_run:
	@python app.py

dev_run_uvicorn:
	@python -m uvicorn app:app --reload

check_code:
	@flake8 .

db_setup_and_load_fixtures:
	@python cli.py mariadb-setup-tables
	@python cli.py database-load-fixtures --chat-app-data
