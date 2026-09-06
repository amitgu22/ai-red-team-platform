import os
os.environ['AUTH_REQUIRED']='false'
from fastapi.testclient import TestClient
from app.main import app

def test_auth_me_dev():
    with TestClient(app) as c:
        r=c.get('/api/auth/me'); assert r.status_code==200; assert r.json()['role']=='admin'

def test_policy_api():
    with TestClient(app) as c:
        r=c.post('/api/platform/policies',json={'name':'test-policy','description':'demo','rules':{'max_risk':80}})
        assert r.status_code in (200,409)
        assert c.get('/api/platform/policies').status_code==200
