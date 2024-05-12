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


class Files(BaseModel):
    file_name:str
    file_path:str
    owner_id:int



class ShareFiles(BaseModel):
    file_name: Optional[str]=None
    shared_to: Optional[str]=None



class ReturnUser(BaseModel):
    id: int
    email: str
    role: str
    created_at: datetime

    class Config:
        orm_mode = True

class ReturnToken(BaseModel):
    access_token: str
    token_type: str

class ResponseFiles(BaseModel):
    id:int
    file_name:str


class ResponseShareFiles(ShareFiles):
    pass


   


    


   
