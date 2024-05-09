from sqlalchemy.orm import Session
from ...pydantic_model import User
from .. import db_model
from ...utils import hash

def get_user(user_email:str, db:Session):

    return db.query(db_model.Users).filter(db_model.Users.email == user_email).first()

def createUser(user: User, db:Session):
    print(user)
    hashedPassword = hash(user.password)
    user.password = hashedPassword
    user = db_model.Users(**user.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


