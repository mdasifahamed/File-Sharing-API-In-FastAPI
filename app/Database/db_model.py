from sqlalchemy import Integer,String,TIMESTAMP,Column
from .database_engine import Base


class Users(Base):

    __tablename__ = 'users'
    
    id = Column(Integer,nullable=False, primary_key=True)
    email = Column(String,nullable=False,unique=True)
    password = Column(String,nullable=False)
    role = Column(String,nullable=False)
    created_at = Column(TIMESTAMP,nullable=False, server_default="now()")
