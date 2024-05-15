import os
from fastapi.testclient import TestClient
from app.main import app

new_client = TestClient(app)

def test_uploadFile(user2_logged_in):
    file = os.getcwd()+'/test/mocks/test.txt'
    print(os.getcwd())

    with open(file,'rb') as uploadFile:
        res = user2_logged_in.post('/file_upload',files={'file':uploadFile})
        assert res.status_code == 200

def test_uploadFail():
    """Here new_client Is not Authenticated And Also No User Is Logged in 
       It's Newly Created Client It As Nothing
    """
    file = os.getcwd()+'/test/mocks/test.txt'
    print(os.getcwd())

    with open(file,'rb') as uploadFile:
        res = new_client.post('/file_upload',files={'file':uploadFile})
        print(res.json())
        assert res.status_code != 200
   

    