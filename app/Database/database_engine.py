import os 
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
load_dotenv()

# Load Environment Variable From .env file 
db_user = os.getenv('db_user')
db_password = os.getenv('db_password')
db_host_name = os.getenv('db_host_name')
db_name = os.getenv('db_name')

# Creating Url for DB Connection
db_url = f"postgresql://{db_user}:{db_password}@{db_host_name}/{db_name}"

# Creating SQLAlchemy Engine That Is Connected To The Database That Will Be Used
db_engine = create_engine(db_url)

''' 
With SQLAlchemy We Can Create Session It Will Can Used    
Anytime  We Want To Do Database Operation From The App
'''
Session = sessionmaker(autoflush=False,bind=db_engine)

'''
It is Base Class For Every Model We Create Using SqlAlchemy To Our Databas. 
Databse Models(Table) That Will Be Created Using SqlAlchemy Will  Inheritet This Class. 
'''
Base = declarative_base()

''' Function To Get DB Session Within The App'''
def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()