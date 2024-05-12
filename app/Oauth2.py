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
#Loading Environment variables
secrect_key = os.getenv('SECRECT_KEY')
algorithm = os.getenv('ALGORITHM')
token_expire_time = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')

# It extarcs the token the login and veriy the user 
# it is used as deepndecies injections
oauth2_schma = OAuth2PasswordBearer(tokenUrl='login')


def createAccessToken(data:dict):
    """Summary or Description of the Function

    Parameters:
    data:(dict)    : data as dictinary whic will be used to createa access token(user_id and user_roel is used to create token)

    Returns:
    encdoed_token(str) : Encoded token


    """
    to_encode = data.copy()
    expire_time = datetime.now(timezone.utc) + timedelta(minutes=int(token_expire_time))
    to_encode.update({'exp': expire_time})#Extending data dictinary with time

    encdoed_token  = jwt.encode(to_encode,secrect_key,algorithm) # creating token as signature

    return encdoed_token

def verifyAccessToken(token:str,credentialException):

    """Summary or Description of the Function

    Parameters:
    token(str)    : token to decode and extract user information

    Returns:
    token_data(dict_object) : retun user data from the token as id and user role which hase been used to create token


    """
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

def get_current_user(token = Depends(oauth2_schma), db: Session=Depends(database_engine.get_db)):
    
    """Summary or Description of the Function

    Parameters:
    token (Depends)    : it depend on oauth2_schma whcih extract token from the login
    db(Session)    : It is an instance of the database session which  will be ijected from the API path.

    Returns:
    user(dict_object) : retun user data from the token after decoding the token

    Using the Fucntion we can get verify and get user data on evevry path we on the app

    """
    credException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="UnAthorized Access", headers={"WWW-AUTHENTICATE":"Bearer"})

    token = verifyAccessToken(token,credException)
    print(token)

    user = db.query(db_model.Users).filter(db_model.Users.id== token.id , db_model.Users.role == token.role).first()

    return user




