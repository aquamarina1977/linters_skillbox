import pytest
from flask import Flask
from task_2 import create_app
from task_2_db_initialization import db
from task_2_models import Client, Parking, ClientParking
from datetime import datetime

@pytest.fixture(scope='module')
def app():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'})
    with app.app_context():
        db.create_all()
        client = Client(name='John', surname='Doe', credit_card='1234-5678-9012-3456', car_number='XYZ123')
        parking = Parking(address='123 Main St', opened=True, count_places=10, count_available_places=10)
        db.session.add_all([client, parking])
        db.session.commit()
    yield app
    with app.app_context():
        db.drop_all()

@pytest.fixture(scope='module')
def client(app):
    return app.test_client()

@pytest.fixture(scope='module')
def db_session(app):
    with app.app_context():
        yield db.session
        db.session.rollback()

@pytest.mark.parametrize('endpoint', ['/clients', '/clients/1'])
def test_get_methods(client, endpoint):
    response = client.get(endpoint)
    assert response.status_code == 200

def test_create_client(client):
    response = client.post('/clients', json={'name': 'Alice', 'surname': 'Smith', 'credit_card': '9876-5432-1098-7654', 'car_number': 'ABC987'})
    assert response.status_code == 201

def test_create_parking(client):
    response = client.post('/parkings', json={'address': '456 Elm St', 'opened': True, 'count_places': 5, 'count_available_places': 5})
    assert response.status_code == 201

@pytest.mark.parking
def test_parking_entry(client, db_session):
    response = client.post('/client_parkings', json={'client_id': 1, 'parking_id': 1})
    assert response.status_code == 201
    parking = db_session.get(Parking, 1)
    assert parking.count_available_places == 9

@pytest.mark.parking
def test_parking_exit(client, db_session):
    client.post('/client_parkings', json={'client_id': 1, 'parking_id': 1})
    response = client.delete('/client_parkings', json={'client_id': 1, 'parking_id': 1})
    assert response.status_code == 200
    parking = db_session.get(Parking, 1)
    assert parking.count_available_places == 10

