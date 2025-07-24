from fastapi.testclient import TestClient
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.main import app


client = TestClient(app)

def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert "HR Resource Query Chatbot" in response.json()["message"]

def test_employee_search():
    response = client.get("/employees/search?skill=Python")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_chat_endpoint():
    response = client.post("/chat", json={"query": "Find Python developers"})
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert "results" in data
