import uuid
from datetime import datetime

from cassandra.cqlengine.models import Model
from cassandra.cqlengine import columns

from config.enviroments import CASSANDRA_CLUSTER_NAME


class User(Model):
    __table_name__ = "Users"
    __keyspace__ = CASSANDRA_CLUSTER_NAME
    __connection__ = CASSANDRA_CLUSTER_NAME

    user_id = columns.UUID(primary_key=True, required=True, default=uuid.uuid4)
    email = columns.Text(max_length=100, required=True, index=True)
    username = columns.Text(max_length=100, required=True, index=True)
    password = columns.Text(max_length=300, required=True)
    created_at = columns.DateTime(default=datetime.now)
    updated_at = columns.DateTime(default=datetime.now)
    last_logged = columns.DateTime(default=datetime.now)
    role_id = columns.UUID(required=True, index=True)
    is_active = columns.Boolean(default=False, index=True)
    banned = columns.Boolean(default=False, index=True)
    created_by = columns.UUID()
