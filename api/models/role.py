from pydantic import BaseModel


class Role(BaseModel):
	name: str
	pseudo_name: str
