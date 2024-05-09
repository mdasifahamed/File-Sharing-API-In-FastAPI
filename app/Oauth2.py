import os
from dotenv import load_dotenv
from jose import jwt,JWTError
from datetime import datetime , timedelta,timezone
from fastapi import HTTPException, Depends ,status
from fastapi.security.oauth2 import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .Database import database_engine
from .Database import db_model
from .pydantic_model import TokenData

load_dotenv()

secrect_key = os.getenv('SECRECT_KEY')
algorithm = os.getenv('ALGORITHM')
token_expire_time = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')


oauth2_schma = OAuth2PasswordBearer(tokenUrl='login')

def createAccessToken(data:dict):
    to_encode = data.copy()
    expire_time = datetime.now(timezone.utc) + timedelta(minutes=int(token_expire_time))
    to_encode.update({'exp': expire_time})

    encdoed_token  = jwt.encode(to_encode,secrect_key,algorithm) 

    return encdoed_token

def verifyAccessToken(token,credentialException):
    try:
        payload = jwt.decode(token,secrect_key,algorithm)
        user_id = payload.get('id')
        user_role = payload.get('role')

        if not id:
            raise credentialException
        
        token_data = TokenData(id=str(user_id),role=str(user_role))

    except JWTError:    

        raise credentialException
    
    return token_data

def get_current_user(token = Depends(oauth2_schma), db: Session=(database_engine.get_db)):
    credException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="UnAthorized Access", headers={"WWW-AUTHENTICATE":"Bearer"})

    token = verifyAccessToken(token,credException)

    user = db.query(db_model.Users).filter(db_model.Users.id== token.id , db_model.Users.role == token.role)

    return user




