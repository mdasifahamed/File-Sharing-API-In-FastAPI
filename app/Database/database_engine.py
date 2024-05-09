import os 
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
load_dotenv()

db_user = os.getenv('db_user')
db_password = os.getenv('db_password')
db_host_name = os.getenv('db_host_name')
db_name = os.getenv('db_name')

db_url = f"postgresql://{db_user}:{db_password}@{db_host_name}/{db_name}"

db_engine = create_engine(db_url)

Session = sessionmaker(autoflush=False,bind=db_engine)

Base = declarative_base()

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()