import os
from dotenv import load_dotenv

from sqlalchemy.engine.url import URL


load_dotenv()

# basics settings
WEB_APP_ADDRESS = os.environ['WEB_APP_ADDRESS']
MARIA_DB_HOST = os.environ['MARIA_DB_HOST']
MARIA_PORT = os.environ['MARIA_PORT']
MARIA_DB_NAME = os.environ['MARIA_DB_NAME']
MARIA_DB_USERNAME = os.environ['MARIA_DB_USERNAME']
MARIA_DB_PASSWORD = os.environ['MARIA_DB_PASSWORD']
MARIA_URL = URL.create(
	drivername="mysql+pymysql",
	username=MARIA_DB_USERNAME,
	password=MARIA_DB_PASSWORD,
	host=MARIA_DB_HOST,
	port=MARIA_PORT,
	database=MARIA_DB_NAME
)

# security settings
SECRET_KEY = os.environ['SECRET_KEY']
SECRET_ALGORITHM = os.environ['SECRET_ALGORITHM']
