import datetime
import json

class Task:
    description: str
    status: str
    id: int
    createdAt: str
    updatedAt: str
        
    def __init__(self, desc, id):
        self.description = desc
        self.id = id
        self.status = "Todo"
        self.createdAt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
        self.updatedAt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") 

    def to_dict(self):
        return {
            "description": self.description,
            "id": self.id,
            "status": self.status,
            "createdAt": self.createdAt,
            "updatedAt": self.updatedAt
        }
