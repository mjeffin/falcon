"""Couldn't get test module working yet. How do I send request body ? Tested with postman
https://github.com/falconry/falcon/pull/748 is the reason why it's not working. Fixed

"""
import json

import falcon
from falcon import testing
import pytest

from service.app import create

@pytest.fixture(scope='module')
def client():
    return testing.TestClient(create())


def test_post_users(client):
    """Test various user signup inputs.Validation is done by marshmallow library and it's default
    validation messages are used wherever applicable"""
    response = client.simulate_post('/users', body="")
    assert response.status == falcon.HTTP_400
    assert set([k for k in response.json["field_errors"].keys()]) == {'password', 'last_name', 'first_name', 'email'}
    missing_field = {"password":"ilovek@ndA!1"}
    response = client.simulate_post('/users', body=json.dumps(missing_field))
    assert response.status == falcon.HTTP_400
    assert set([k for k in response.json["field_errors"].keys()]) == {'last_name', 'first_name', 'email'}
    incorrect_field = {
        "first_name": 200,
        "last_name": "Holmes2",
        "email": "sherlock@example.com",
        "password": "ilovendA@1"
    }
    response = client.simulate_post('/users', json=incorrect_field)
    assert response.status == falcon.HTTP_400
    assert set([k for k in response.json["field_errors"].keys()]) == {'first_name'}
    short_password = {
        "first_name": "Sherlock",
        "last_name": "Holmes2",
        "email": "sherlock@example.com",
        "password": "a"
    }
    response = client.simulate_post('/users', json=short_password)
    assert response.status == falcon.HTTP_400
    expected_json = {
        "error": "Bad request",
        "field_errors": {
            "password": [
                "password must be at least 8 characters"
            ]
        }
    }
    assert response.status == falcon.HTTP_400
    assert response.json == expected_json
    invalid_email = {
        "first_name": "Sherlock",
        "last_name": "Holmes2",
        "email": "a@b.c",
        "password": "ilovendA@1"
    }
    response = client.simulate_post('/users', json=invalid_email)
    assert response.status == falcon.HTTP_400
    assert set([k for k in response.json["field_errors"].keys()]) == {'email'}
    valid_request = {
        "first_name": "sherlock",
        "last_name": "Holmes",
        "email": "sherlock@example.com",
        "password": "ilovendA@1"
    }
    response = client.simulate_post('/users', json=valid_request)
    assert response.status == falcon.HTTP_201



