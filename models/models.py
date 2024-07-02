from pydantic import BaseModel

class History(BaseModel): 
    user_id: str
    description: str
    description_embedding: list[float]


class User(BaseModel): 
    first_name: str
    last_name: str
    description: str
    description_embedding: list[float]