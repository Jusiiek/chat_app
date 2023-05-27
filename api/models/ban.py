from pydantic import BaseModel

from models import User

class Ban(BaseModel):
	user: User
	reason: str
	ban_expire: str