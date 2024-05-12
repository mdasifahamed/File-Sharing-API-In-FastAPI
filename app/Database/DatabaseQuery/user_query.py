from sqlalchemy.orm import Session
from ...pydantic_model import User
from .. import db_model
from ...utils import hash

def get_user(user_email:str, db:Session):

    return db.query(db_model.Users).filter(db_model.Users.email == user_email).first()

def createUser(user: User, db:Session):


    """Summary or Description of the Function

    Parameters:
    user (User)    : Pydantic model which contain payload from the request to the server
    db(Session)    : It is an instance of the database session which  will be ijected from the API path.
    user(dict_objcet) : Return the new user object

    """

    hashedPassword = hash(user.password) # hash plain plain text password to encryted form to store it on the db
    user.password = hashedPassword # updating the password with hashed string
    user = db_model.Users(**user.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


