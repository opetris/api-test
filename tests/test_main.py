#coding : utf-8
from fastapi.testclient import TestClient
from restoapp.main import define_app

app = define_app()
client = TestClient(app)

def test_correct_get_request():
    response = client.get('/search/?lat=48.8319929&long=2.3245488&rad=100')
    assert response.status_code == 200

def test_incorrect_get_request():
    response = client.get('/')
    assert response.status_code == 404

