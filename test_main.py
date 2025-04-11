import pytest
from fastapi.testclient import TestClient
from routes import app
from db_setup import Base, engine, SessionLocal

client = TestClient(app)

# Create a fresh DB before running tests
@pytest.fixture(scope="module", autouse=True)
def setup_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

# Store auth token between tests
auth_token = None
created_post_id = None
created_comment_id = None

def test_register_user():
    response = client.post("/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "securepass"
    })
    assert response.status_code == 200
    assert response.json()["msg"] == "User created"

def test_duplicate_registeration():
    response = client.post("/register", json={
        "username": "testuser2",
        "email": "test@example.com",
        "password": "anotherpass"
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

def test_login():
    global auth_token
    response = client.post("/login", data={
        "username": "test@example.com", #OAuth2PasswordRequestForm uses `username`
        "password": "securepass"
    })
    assert response.status_code == 200
    auth_token = response.json()["access_token"]
    assert auth_token

def test_create_post():
    global created_post_id
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.post("/posts", json={
        "title": "My First Post",
        "content": "Hello World!"
    }, headers=headers)
    assert response.status_code == 200
    assert "Post created" in response.json()["msg"]

def test_get_post():
    response = client.get("/posts")
    assert response.status_code == 200
    posts = response.json()["posts"]
    assert isinstance(posts, list)
    assert posts[0]["title"] == "My First Post"

def test_comment_post():
    global created_comment_id
    headers = {"Authorization": f"Bearer {auth_token}"}
    post_id = client.get("/posts").json()["posts"][0]["id"]
    response = client.post(f"/posts/{post_id}/comments", json={
        "content": "Great post!"
    }, headers=headers)
    assert response.status_code == 200
    created_comment_id = response.json()["comment"]

def test_get_comments():
    post_id = client.get("/posts").json()["posts"][0]["id"]
    response = client.get(f"/posts/{post_id}/comments")
    assert response.status_code == 200
    assert len(response.json()["comments"]) > 0

def test_delete_post():
    headers = {"Authorization": f"Bearer {auth_token}"}
    post_id = client.get("/posts").json()["posts"][0]["id"]
    response = client.delete(f"/posts/{post_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["msg"] == "Post deleted"

def test_delete_comment():
    headers = {"Authorization": f"Bearer {auth_token}"}
    comments = client.get("/posts/1/comments").json().get("comments", [])
    if comments:
        comment_id = comments[0]["id"]
        response = client.delete(f"/comments/{comment_id}", headers=headers)
        assert response.status_code == 200
        assert response.json()["msg"] == "Comment deleted"