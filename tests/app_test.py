import pytest

from app import create_app, db
from app.models import Result
import json

from app.routes import bp


@pytest.fixture
def client():
    test_config = {
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False
    }

    app = create_app(test_config)
    app.register_blueprint(bp)  # Регистрация блюпринта с роутами

    with app.app_context():
        db.create_all()

    with app.test_client() as client:
        yield client


def test_ping(client):
    response = client.get('/ping')
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_submit_success(client):
    payload = {"name": "Test User", "score": 42}
    response = client.post(
        '/submit', data=json.dumps(payload), content_type='application/json')
    assert response.status_code == 201
    assert "message" in response.get_json()


def test_submit_invalid_data(client):
    payload = {"name": "Test User"}  # отсутствует score
    response = client.post(
        '/submit', data=json.dumps(payload), content_type='application/json')
    assert response.status_code == 400
    assert "error" in response.get_json()


def test_submit_invalid_score(client):
    payload = {"name": "Test User", "score": "invalid"}
    response = client.post(
        '/submit', data=json.dumps(payload), content_type='application/json')
    assert response.status_code == 400
    assert "error" in response.get_json()


def test_results(client):
    # Добавим данные вручную
    with client.application.app_context():
        db.session.add(Result(name="Alice", score=90))
        db.session.commit()

    response = client.get('/results')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert data[0]['name'] == "Alice"
    assert data[0]['score'] == 90
