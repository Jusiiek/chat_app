import os
from dotenv import load_dotenv


load_dotenv()

# basics settings
WEB_APP_ADDRESS = os.environ['WEB_APP_ADDRESS']
MONGO_URL = os.environ['MONGO_URL']

# security settings
SECRET_KEY = os.environ['SECRET_KEY']
SECRET_ALGORITHM = os.environ['SECRET_ALGORITHM']
