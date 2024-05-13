from fastapi.testclient import TestClient
from app.main import app

test_client = TestClient(app)
def test_root():
   r = test_client.get('/')
   print(r.json())
   assert r.json().get('status') == 'Okay'
   assert r.status_code == 200

   