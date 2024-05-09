from fastapi import FastAPI,Depends,status,HTTPException
from sqlalchemy.orm import Session
from .Database.database_engine import db_engine,get_db
from .Database import db_model
from .router import users,login
from .Oauth2 import get_current_user
from .pydantic_model import ReturnUser

app = FastAPI()

db_model.Base.metadata.create_all(bind=db_engine)

app.include_router(users.router)
app.include_router(login.router)

@app.get('/')
async def root():
    return {'status':'Okay'}


@app.get('/testdb')
async def testconnect(db: Session = Depends(get_db)):

    posts = db.query(db_model.Users).all()
    print(posts)
    return{'status': 'okay'}


# protected paths
@app.get('/onlyadmin')

async def onlyadmin(current_user = Depends(get_current_user)):
    user_role = current_user.role
    if user_role.lower() != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Not A Admin")
    return {'access_type':'admin'}

@app.get('/onlymoderator')

async def onlymoderator(current_user = Depends(get_current_user)):
    user_role = current_user.role

    if user_role.lower() != 'moderator':

        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Not A Moderator")
    
    return {'access_type':'moderator'}


@app.get('/onlyuser')
async def onlyuser(current_user = Depends(get_current_user)):
    user_role = current_user.role

    if user_role.lower() != 'user':

        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Not A User")
    
    return {'access_type':'user'}

    
