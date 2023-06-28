from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config.enviroments import MARIA_URL

# seconds
SQLALCHEMY_CONNECTION_TIMEOUT = 60
mysql_engine = create_engine(
	MARIA_URL,
	connect_args=dict(
		connect_timeout=SQLALCHEMY_CONNECTION_TIMEOUT,
		use_unicode=True
	),
	pool_size=20,
	max_overflow=5,
)

# pool_size: Specifies the number of database connections to pool.
# max_overflow: Sets the maximum number of connections that can be created beyond the pool_size when needed.
# This allows for handling occasional spikes in connection demand.

CHAT_APP_SESSION = sessionmaker(bind=mysql_engine)

def get_sql_db():
	db = CHAT_APP_SESSION()
	try:
		yield db
	finally:
		db.close()
