from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from cassandra.cluster import Cluster, ExecutionProfile, EXEC_PROFILE_DEFAULT
from cassandra.policies import WhiteListRoundRobinPolicy, DowngradingConsistencyRetryPolicy
from cassandra.query import tuple_factory
from cassandra.auth import PlainTextAuthProvider

from config.enviroments import (
	MARIA_URL,
	DB_HOST,
	CASSANDRA_DB_USERNAME,
	CASSANDRA_DB_PASSWORD,
	CASSANDRA_PORT
)

# seconds
SQLALCHEMY_CONNECTION_TIMEOUT = 60

# pool_size: Specifies the number of database connections to pool.
# max_overflow: Sets the maximum number of connections that can be created beyond the pool_size when needed.
# This allows for handling occasional spikes in connection demand.
mysql_engine = create_engine(
	MARIA_URL,
	connect_args=dict(
		connect_timeout=SQLALCHEMY_CONNECTION_TIMEOUT,
		use_unicode=True
	),
	pool_size=20,
	max_overflow=5,
)
CHAT_APP_SESSION = sessionmaker(bind=mysql_engine)


node1_profile = ExecutionProfile(load_balancing_policy=WhiteListRoundRobinPolicy(['0.0.0.1']),
                                 request_timeout=10)
node2_profile = ExecutionProfile(load_balancing_policy=WhiteListRoundRobinPolicy(['0.0.0.2']),
                                 request_timeout=10)
profiles = {'node1': node1_profile, 'node2': node2_profile}

auth_provider = PlainTextAuthProvider(
	username=CASSANDRA_DB_USERNAME,
	password=CASSANDRA_DB_PASSWORD
)
cluster = Cluster(
	[DB_HOST],
	port=CASSANDRA_PORT,
	auth_provider=auth_provider,
	execution_profiles=profiles
)
cassandra_session = cluster.connect()


def get_sql_db():
	db = CHAT_APP_SESSION()
	try:
		yield db
	finally:
		db.close()
