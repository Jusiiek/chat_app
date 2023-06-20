import os
from dotenv import load_dotenv


load_dotenv()

# basics settings
WEB_APP_ADDRESS = os.environ['WEB_APP_ADDRESS']
CLUSTER_NAME = os.environ['CLUSTER_NAME']
DB_USERNAME = os.environ['DB_USERNAME']
DB_PASSWORD = os.environ['DB_PASSWORD']

# security settings
SECRET_KEY = os.environ['SECRET_KEY']
SECRET_ALGORITHM = os.environ['SECRET_ALGORITHM']
