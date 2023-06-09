import uuid

from datetime import datetime

from cassandra.cqlengine.models import Model
from cassandra.cqlengine import columns

from config.enviroments import CASSANDRA_CLUSTER_NAME


class Ban(Model):
	__table_name__ = "Bans"
	__keyspace__ = CASSANDRA_CLUSTER_NAME
	__connection__ = CASSANDRA_CLUSTER_NAME

	ban_id = columns.UUID(primary_key=True, required=True, default=uuid.uuid4)
	user_id = columns.Integer(required=True)
	reason = columns.Text(max_length=300, required=True)
	created_by = columns.Integer(required=True)
	created_at = columns.DateTime(default=datetime.now)
	ban_expire = columns.DateTime()
	is_permanently_banned = columns.Boolean(default=False)
