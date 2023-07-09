from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from cassandra.cluster import Cluster, ExecutionProfile
from cassandra.policies import WhiteListRoundRobinPolicy
from cassandra.auth import PlainTextAuthProvider
from cassandra.cqlengine import connection
from cassandra.cqlengine.management import create_keyspace_simple

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
# max_overflow: Sets the maximum number of connections
# that can be created beyond the pool_size when needed.
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


def get_sql_db():
	db = CHAT_APP_SESSION()
	try:
		yield db
	finally:
		db.close()


node1_profile = ExecutionProfile(
	load_balancing_policy=WhiteListRoundRobinPolicy(['0.0.0.1']), request_timeout=10
)
node2_profile = ExecutionProfile(
	load_balancing_policy=WhiteListRoundRobinPolicy(['0.0.0.2']), request_timeout=10
)
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


def cassandra_connect():
	session = cluster.connect()
	connection.register_connection('chatapp', session=session)
	create_keyspace_simple(
		name="chatapp", connections=["chatapp"], replication_factor=4
	)


def cassandra_close():
	cluster.shutdown()
	connection.unregister_connection('chatapp')
