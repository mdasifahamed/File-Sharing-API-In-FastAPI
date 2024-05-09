from pydantic import BaseModel,EmailStr
from datetime import datetime


class User(BaseModel):
    email: EmailStr
    password: str
    role: str

class ReturnUser(BaseModel):
    id: int
    email: str
    role: str
    created_at: datetime

    class Config:
        from_attributes = True

    


   
