import uuid
from datetime import datetime

from cassandra.cqlengine.models import Model
from cassandra.cqlengine import columns


class User(Model):
    __table_name__ = "Users"

    user_id = columns.UUID(primary_key=True, required=True, default=uuid.uuid4)
    email = columns.Text(max_length=100, required=True)
    username = columns.Text(max_length=100, required=True)
    password = columns.Text(max_length=300, required=True)
    created_at = columns.DateTime(default=datetime.now)
    updated_at = columns.DateTime(default=datetime.now)
    last_logged = columns.DateTime(default=datetime.now)
    role_id = columns.Integer(required=True)
    is_active = columns.Boolean(default=False)
    banned = columns.Boolean(default=False)
