from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from app.config import settings
from app.database import get_db
from app.database import Base
from fastapi.testclient import TestClient
from app.main import app
import pytest
from app.oauth2 import create_access_token
from app.models import Post

database_url = settings.database_url

if database_url.startswith("postgresql://"):
    database_url = database_url.replace(
        "postgresql://",
        "postgresql+psycopg://",
        1
    )

DATABASE_URL = f"{database_url}_test"

engine = create_engine(DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user2(client):
    user_data = {"email": "sanjeev123@gmail.com",
                 "password": "password123"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201

    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture
def test_user(client):
    user_data = {"email": "atharv@gmail.com", "password": "1234"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['user_id']})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client


@pytest.fixture
def test_posts(test_user, session, test_user2):
    posts_data = [
        {"title": "First Post", "content": "Content of the first post",
            "owner_id": test_user['user_id']},
        {"title": "Second Post", "content": "Content of the second post",
            "owner_id": test_user['user_id']},
        {"title": "Third Post", "content": "Content of the third post",
            "owner_id": test_user['user_id']},
        {"title": "Fourth Post", "content": "Content of the fourth post",
            "owner_id": test_user2['user_id']}
    ]

    def create_post_models(post):
        return Post(**post)

    all_posts = list(map(create_post_models, posts_data))
    session.add_all(all_posts)
    session.commit()

    return session.query(Post).all()
