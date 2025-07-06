import pytest
from fastapi.testclient import TestClient
from main import Base, get_db, app
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os


load_dotenv()

DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
TEST_DB_NAME = os.getenv("TEST_DB_NAME")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")


TEST_DB_URL = f"postgresql+psycopg://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{TEST_DB_NAME}"

# Test DB connection
test_engine = create_engine(TEST_DB_URL)
testingLocalSession = sessionmaker(autocommit=False, autoflush=False, bind= test_engine)

#Depedency ovverride to test DB
def override_get_db():
    db = testingLocalSession()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client():
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)

def register_and_login(client, username = "testuser", password = "testpass"):
    client.post('/register', json = {"username": username, "password": password})

    response = client.post('/token', data = {"username": username, "password": password})
    token = response.json()['access_token']
    return {"Authorization": f"Bearer {token}"}

def test_register_and_login_invalid_user(client, username = "testuser", password = "testpass"):
      client.post('/register', json = {"username": username, "password": password})

      response = client.post('/token', data = {"username": username, "password": "Incorrent_password"})
      assert response.status_code == 401
      assert "incorrect username or password" in response.json()["detail"].lower()

def test_create_task(client):
        headers =  register_and_login(client)

        response = client.post('/tasks/', json = {"title": "task1", "description": "This is the first task", "completed": False}, headers = headers)
        assert response.status_code == 200
        assert response.json()['title'] == "task1"
        assert response.json()['description'] == "This is the first task"
        assert response.json()['completed'] == False

def test_get_task(client):
        headers =  register_and_login(client)
        client.post('/tasks/', json = {"title": "task1", "description": "This is the first task", "completed": False}, headers = headers)

        response = client.get('/tasks/1',headers=headers)
        assert response.status_code == 200
        assert response.json()['title'] == "task1"
        assert response.json()['description'] == "This is the first task"
        assert response.json()['completed'] == False

def test_cannot_access_others_tasks(client):
      headers_user1 = register_and_login(client, username= "user1", password= "password1")
      client.post('/tasks', json = {"title": "task1", "description": "This is the first task", "completed": False}, headers = headers_user1)

      headers_user2 = register_and_login(client, username= "user2", password="password2")
      response = client.get('/tasks/1', headers = headers_user2)

      assert response.status_code == 404

def test_update_nonexistent_task(client):
      headers = register_and_login(client)
      client.post('/tasks/', json = {"title": "task1", "description": "This is the first task", "completed": False}, headers = headers)

      response = client.put('/tasks/2',json=  {"title": "Updated task", "description": "Updated description", "completed": True},headers=headers)
      assert response.status_code == 404


def test_delete_task(client):
        headers =  register_and_login(client)
        client.post('/tasks/', json = {"title": "task1", "description": "This is the first task", "completed": False}, headers = headers)

        response = client.delete('/tasks/1',headers=headers)
        assert response.status_code == 200
        assert "deleted" in response.json()["message"].lower()