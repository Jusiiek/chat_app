import os
from dotenv import load_dotenv

load_dotenv()

WEB_APP_ADDRESS = os.environ['WEB_APP_ADDRESS']
MONGO_URL = os.environ['MONGO_URL']
