from pydantic import BaseModel
from datetime import datetime


class Ban(BaseModel):
	username: str
	reason: str
	ban_expire: datetime
	ban_expire_str: str
