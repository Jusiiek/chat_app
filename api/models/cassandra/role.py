import uuid

from cassandra.cqlengine.models import Model
from cassandra.cqlengine import columns

from config.enviroments import CASSANDRA_CLUSTER_NAME


class Role(Model):
	__table_name__ = "Roles"
	__keyspace__ = CASSANDRA_CLUSTER_NAME
	__connection__ = CASSANDRA_CLUSTER_NAME

	role_id = columns.UUID(primary_key=True, required=True, default=uuid.uuid4)
	name = columns.Text(max_length=20, required=True)
	pseudo_name = columns.Text(max_length=20, required=True)
