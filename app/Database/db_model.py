from sqlalchemy import Integer,String,TIMESTAMP,Column,ForeignKey # Data types For Database Table 
from .database_engine import Base # the base created At database_engine module



'''
'Users' Class is representation Of 
Users table in the database
It has columns 'id', 'email', 'password'(hashed Password),'role'(user role), 
'createted_at'(time of creating User profile).
'''
class Users(Base):

    __tablename__ = 'users' # actual table name in the database
    
    id = Column(Integer,nullable=False, primary_key=True)
    email = Column(String,nullable=False,unique=True) # email column is made unique so that a user with smae cannot have multiple account one email one user
    password = Column(String,nullable=False)
    role = Column(String,nullable=False)
    created_at = Column(TIMESTAMP,nullable=False, server_default="now()")



'''
'Files' Class is representation Of 
files table in the database.it Stores information About The Uploaded File
It has columns 'id', 'file_name', 'file_path'(the path where the file is stored on app serever)
'owner_id'(the user who has uploaded the file is the owner of file)
'''
class Files(Base):
    __tablename__ = 'files'# actual table name in the database

    id = Column(Integer,nullable=False,primary_key=True)
    file_name = Column(String,nullable=False)
    file_path = Column(String,nullable=False)
    owner_id = Column(Integer,ForeignKey('users.id',ondelete='CASCADE'), nullable=False)


'''
'SharedFiles' Class is representation Of 
shared_file table in the database it stores the information about the file that has been shared with other user.
It has columns 'file_id'(which is the id of the file that has been shared with someone within the app),
'shared_to' ,(the person to whom the file has been shared we), 
'shared_by'(who shred the file in this app only file onwer can share the file)
'''

class SharedFiles(Base):
     
    __tablename__ = 'shared_files'# actual table name in the db

    file_id =  Column(Integer,nullable=False,primary_key=True)

    shared_to = Column(String,nullable=False)
    
    shared_by = Column(String,nullable=False)


