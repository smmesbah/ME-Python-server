from pydantic import BaseModel

class History(BaseModel): 
    user_id: str
    description: str
    description_embedding: list[float]

class PostHistory(BaseModel):
    user_id: str
    description: str


class User(BaseModel): 
    first_name: str
    last_name: str
    description: str
    description_embedding: list[float]

class Todo(BaseModel):
    user_id: str
    taskTitle: str
    taskColor: str
    startDate: str
    endDate: str
    startTime: str
    endTime: str
    reminderTime: str
    taskType: str
    tag: str
    label: str
    redirectURL: str
    progress: int
    priority: str