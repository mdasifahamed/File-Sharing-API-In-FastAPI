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


@pytest.fixture(scope='module')
def client():
    print("From client")
        
    Base.metadata.create_all(bind=db_engine)
    yield TestClient(app)
    Base.metadata.drop_all(bind=db_engine)


# Dummy User 1
@pytest.fixture(scope='module')
def test_user1(client):
    user={'email':'dummy_user1@ymail.com','password':'password123','role':'admin'}
    res = client.post('/register', json =user)
    test_user1 = res.json()

    assert res.status_code ==  201

    test_user1['password'] = user['password']
    return test_user1

# Dummy User 2
@pytest.fixture(scope='module')
def test_user2(client):
    user={'email':'dummy_user2@ymail.com','password':'password123','role':'admin'}
    res = client.post('/register', json =user)
    test_user1 = res.json()

    assert res.status_code ==  201

    test_user1['password'] = user['password']
    return test_user1


# Dummy User 3
@pytest.fixture(scope='module')
def test_user3(client):
    user={'email':'dummy_user3@ymail.com','password':'password123','role':'user'}
    res = client.post('/register', json =user)
    test_user1 = res.json()

    assert res.status_code ==  201

    test_user1['password'] = user['password']
    return test_user1


""" All The user_looged_in fixture returns a client

    As The API Only Permits To Upload And Share Files Between The Users
    Of The API. And the API Seeks Token Authentication. The Client Created At The Top
    Is Updated Here With The Authentication Headers For Further Tests

    Steps Done Here
    1. log a user with created from the test_user fixtrues
    2.  '/login' path returns Dict of JWT token and token_bearer type
    3. Extract the token from the response from the '/login'
    4. Updated the client header with the token
    5. Returned The Same Updated Client

    Same proccess is applied for fixtures user1_looged_in, user2_looged_in user3_looged_in
"""

@pytest.fixture(scope='module')
def user1_logged_in(test_user1,client):
    
    res = client.post('/login',data = {'username':test_user1['email'],'password':test_user1['password']})
    token = res.json().get('access_token')
    client.headers.update({"Authorization":f'Bearer {token}'})
    return client

@pytest.fixture(scope='module')
def user2_logged_in(test_user2,client):
    
    res = client.post('/login',data = {'username':test_user2['email'],'password':test_user2['password']})
    token = res.json().get('access_token')
    client.headers.update({"Authorization":f'Bearer {token}'})
    return client

@pytest.fixture(scope='module')
def user3_logged_in(test_user3,client):
    
    res = client.post('/login',data = {'username':test_user3['email'],'password':test_user3['password']})
    token = res.json().get('access_token')
    client.headers.update({"Authorization":f'Bearer {token}'})
    return client

@pytest.fixture(scope='module')
def user1_file_upload(user1_logged_in):
    file = os.getcwd()+'/test/mocks/test.txt'
    with open(file,'rb') as uploadFile:
        res = user1_logged_in.post('/file_upload', files = {'file':uploadFile})
        return res.json()

   





