"""Couldn't get test module working yet. How do I send request body ? Tested with postman"""
import falcon
from falcon import testing
import pytest

from service.app import app

@pytest.fixture
def client():
    return testing.TestClient(app)

# pytest will inject the object returned by the "client" function
# as an additional parameter.
def test_post_users(client):
    hdrs = [('Accept', 'application/json'),
            ('Content-Type', 'application/json'), ]
    empty_body = {}
    # response = client.simulate_post('/users')
    # assert response.status == falcon.HTTP_400
    missing_fields = {"password":"ilovek@ndA!1"}
    response = client.simulate_post('/users',)
    assert response.status == falcon.HTTP_400