import uuid

from cassandra.cqlengine.models import Model
from cassandra.cqlengine import columns

from config.enviroments import CASSANDRA_CLUSTER_NAME


class Role(Model):

	ROLE_ADMIN = "ADMIN"
	ROLE_SUBSCRIBER_PLUS = "SUBSCRIBER_PLUS"
	ROLE_SUBSCRIBER = "SUBSCRIBER"
	ROLE_USER = "USER"

	__table_name__ = "Roles"
	__keyspace__ = CASSANDRA_CLUSTER_NAME
	__connection__ = CASSANDRA_CLUSTER_NAME

	role_id = columns.UUID(primary_key=True, required=True, default=uuid.uuid4)
	name = columns.Text(max_length=20, required=True, index=True)
	pseudo_name = columns.Text(max_length=20, required=True)
