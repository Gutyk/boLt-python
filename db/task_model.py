from beanie import Document
from typing import Optional 


class Task(Document):
    user_id: int
    title: str
    description: Optional[str] = None
    completed: bool = False
    
    class Settings:
        name = "tasks"