from fastapi import APIRouter,HTTPException,Depends,status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..Database import database_engine
from ..Database import db_model
from ..pydantic_model import ReturnToken
from ..utils import authenticate
from ..Oauth2 import createAccessToken


router = APIRouter(
    tags=['Login']
)


@router.post('/login',status_code=status.HTTP_201_CREATED,response_model=ReturnToken)
async def login(user_credential:OAuth2PasswordRequestForm = Depends(), 
db : Session=Depends(database_engine.get_db)):
    
    user = db.query(db_model.Users).filter(db_model.Users.email == user_credential.username).first()

    # if Email Addess Is Not Valid Then Throw Error
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid Credential")
    
    # if Password Is Not Valid Then Throw Error
    if not authenticate(user_credential.password,user.password):

        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            
                            detail=f"Invalid Credential")
    
    token = createAccessToken(data={'id': user.id, 'role':user.role})

    tokendata = ReturnToken(access_token=token,token_type="bearer")

    return tokendata