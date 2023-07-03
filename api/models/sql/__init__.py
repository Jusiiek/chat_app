from sqlalchemy.ext.declarative import declarative_base

from config.db_config import mysql_engine

Base = declarative_base(bind=mysql_engine)
