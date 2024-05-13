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
    

def test_register_user(client):
    r = client.post('/register',json={"email":'dummyuser@gmail.com', 'password':'password123','role':'admin'})
    
    new_user = pydantic_model.ReturnUser(**r.json())
    assert new_user.role == 'admin'
    assert new_user.email == 'dummyuser@gmail.com'

def test_log(client):
    # at login OAuth2PasswordRequestForm is used whihc expect username and password as formdata

    r = client.post('/login',data={"username":'dummyuser@gmail.com','password':'password123'})
    token = r.json().get('access_token')
    # decode the token and return the info 
    payload = jwt.decode(token,secrect_key,algorithm)
    user_role = payload.get('role')
    assert user_role == 'admin'
    assert r.status_code == 201




    