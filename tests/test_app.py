import pytest
import json
from app import create_app, db

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "JWT_SECRET_KEY": "test-secret-key",
        "SECRET_KEY": "test-secret-key",
        "BCRYPT_LOG_ROUNDS": 4,
        "MAIL_SUPPRESS_SEND": True
    })

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_app_creation(app):
    assert app is not None
    assert app.config["TESTING"]

def test_register(client):
    """Test user registration."""
    res = client.post('/auth/register', data=json.dumps({
        "name": "Test User",
        "email": "test@example.com",
        "password": "password",
        "role": "client"
    }), content_type='application/json')
    response_json = res.get_json()
    print(f"Register response: {response_json}")
    assert res.status_code == 201
    assert "User created" in response_json["msg"]

def test_login_unverified(client):
    """Test login with an unverified email."""
    # First, register a user
    client.post('/auth/register', data=json.dumps({
        "name": "Test User",
        "email": "test@example.com",
        "password": "password",
        "role": "client"
    }), content_type='application/json')

    # Then, try to log in
    res = client.post('/auth/login', data=json.dumps({
        "email": "test@example.com",
        "password": "password"
    }), content_type='application/json')
    assert res.status_code == 401
    assert "Account not verified" in res.get_json()["msg"]