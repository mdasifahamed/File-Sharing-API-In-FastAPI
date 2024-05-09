from fastapi import FastAPI,Depends
from sqlalchemy.orm import Session
from .Database.database_engine import db_engine,get_db
from .Database import db_model

from .router import users,login

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