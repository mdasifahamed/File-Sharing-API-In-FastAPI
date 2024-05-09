from pydantic import BaseModel,EmailStr
from typing import Optional
from datetime import datetime


class User(BaseModel):
    email: EmailStr
    password: str
    role: str



class TokenData(BaseModel):
    id: Optional[str] = None
    role: Optional[str] = None
    
class ReturnUser(BaseModel):
    id: int
    email: str
    role: str
    created_at: datetime

    class Config:
        from_attributes = True

class ReturnToken(BaseModel):
    access_token: str
    token_type: str


    


   
