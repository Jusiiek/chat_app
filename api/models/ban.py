from pydantic import BaseModel

from models.user import User

class Ban(BaseModel):
	user: User
	reason: str
	ban_expire: str