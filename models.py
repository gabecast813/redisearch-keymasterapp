from pydantic import BaseModel
from typing import List, Optional

class User(BaseModel):
    id: int
    username: str
    first_name: str
    last_name: str
    email: str
    display_name: str
    user_type: str

class SearchResponse(BaseModel):
    users: List[User]
    count: int