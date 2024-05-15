import os,pytest
from fastapi.testclient import TestClient
from jose import jwt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,Session
from dotenv import load_dotenv
from app.main import app
from app.Database.database_engine import get_db
from app.Database.db_model import Base, Users
from app import pydantic_model

load_dotenv()

# Load Environment Variable From .env file 
db_user = os.getenv('db_user')
db_password = os.getenv('db_password')
db_host_name = os.getenv('db_host_name')
db_name = os.getenv('db_test_db_name')
secrect_key = os.getenv('SECRECT_KEY')
algorithm = os.getenv('ALGORITHM')
token_expire_time = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')
db_url = f"postgresql://{db_user}:{db_password}@{db_host_name}/{db_name}"


db_engine = create_engine(db_url)


TestSession = sessionmaker(autoflush=False,bind=db_engine)


''' Function To Get DB Session Within The App'''
def override_get_db():
    db = TestSession()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="module")
def client():
        
    Base.metadata.create_all(bind=db_engine)
    yield TestClient(app)
    Base.metadata.drop_all(bind=db_engine)

@pytest.fixture(scope='module')
def test_user1(client):
    user={'email':'dummy_user1@ymail.com','password':'password123','role':'admin'}
    res = client.post('/register', json =user)
    test_user1 = res.json()

    assert res.status_code ==  201

    test_user1['password'] = user['password']
    return test_user1


