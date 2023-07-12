from datetime import datetime

from pydantic import BaseModel


class BanSchema(BaseModel):
	reason: str
	created_at: datetime
	ban_expire: datetime
