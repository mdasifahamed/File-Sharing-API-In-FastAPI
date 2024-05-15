import pytest
from app import pydantic_model
from jose import jwt 
import os 
from dotenv import load_dotenv

load_dotenv()
secrect_key = os.getenv('SECRECT_KEY')
algorithm = os.getenv('ALGORITHM')
token_expire_time = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')

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

@pytest.mark.parametrize('email,password,status_code',[
    (None,"password123",422),
    ('dummyuser@gmail.com',"password",403)
])
def test_invalid_login(client, email,password,status_code):
    res = client.post('/login',data={"username":email,'password':password})
    assert res.status_code == status_code

def test_test_user_login(client,test_user1):

    res = client.post('/login', data={'username': test_user1['email'] ,'password': test_user1['password']})
    token = res.json().get('access_token')
    # decode the token and return the info 
    payload = jwt.decode(token,secrect_key,algorithm)
    user_role = payload.get('role')
    print(test_user1['email'])
    assert user_role == 'admin'
    assert res.status_code == 201


