from fastapi import APIRouter,HTTPException,status,Depends
from sqlalchemy.orm import Session
from ..Database import database_engine
from ..Database.DatabaseQuery import user_query
from ..pydantic_model import User,ReturnUser

router = APIRouter(
    tags=["USER"]
)

@router.post('/register',status_code=status.HTTP_201_CREATED,response_model=ReturnUser)

def createUser(user:User,db: Session=Depends(database_engine.get_db)):
  
    exiting_user = user_query.get_user(user.email,db)
    
    if exiting_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f'User Already Exists With Email : {user.email}')
    
    new_user = user_query.createUser(user,db)

    return new_user


