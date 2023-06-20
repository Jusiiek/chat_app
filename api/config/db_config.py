from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

from config.enviroments import CLUSTER_NAME, DB_USERNAME, DB_PASSWORD


auth_provider = PlainTextAuthProvider(username=DB_USERNAME, password=DB_PASSWORD)
cluster = Cluster(['0.0.0.0'], auth_provider=auth_provider)

def connect_db():
	return cluster.connect()


def close_connection():
	return cluster.shutdown()
