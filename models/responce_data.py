from typing import List, Optional
from pydantic import BaseModel


class User(BaseModel):
    name: str
    surname: str
    age: int
    phone: str


class ResponseData(BaseModel):
    id: Optional[str]
    method: Optional[str]
    reason: Optional[str]
    status: str
    users: Optional[List[User]]
