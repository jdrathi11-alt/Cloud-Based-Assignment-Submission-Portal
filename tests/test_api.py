import os
os.environ["DATABASE_URL"]="sqlite:///./test_portal.db"
os.environ["STORAGE_MODE"]="local"
os.environ["LOCAL_UPLOAD_DIR"]="./test_uploads"
from fastapi.testclient import TestClient
from backend.app.main import app

client=TestClient(app)

def test_health():
    r=client.get('/health'); assert r.status_code==200; assert r.json()['status']=='ok'

def test_register_and_login():
    email='student@example.com'
    r=client.post('/api/register',json={'name':'Test Student','email':email,'password':'password123','role':'student'})
    assert r.status_code in (201,409)
    r=client.post('/api/login',json={'email':email,'password':'password123'})
    assert r.status_code==200
    assert 'access_token' in r.json()
