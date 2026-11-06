from fastapi.testclient import TestClient
from src.api.main import app
client=TestClient(app)
def test_health():assert client.get('/health').json()['status']=='ok'
def test_invalid():assert client.post('/ask',json={'question':'x'}).status_code==422
def test_unknown():assert 'do not have' in client.post('/ask',json={'question':'Tell me about parking facilities'}).json()['answer']
