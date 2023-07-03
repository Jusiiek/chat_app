import uuid
from datetime import datetime

from cassandra.cqlengine.models import Model
from cassandra.cqlengine import columns

class Token(Model):
	__table_name__ = 'Tokens'

	token_id = columns.UUID(primary_key=True, default=uuid.uuid4)
	token = columns.Text(max_length=300, required=True)
	expired_at = columns.DateTime(required=True)