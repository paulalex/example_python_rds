"""
Test the users blueprint.

These tests use GETs and POSTs to different URLs to check for the proper behavior
of the users blueprint.
"""
import json

from test_config import test_client
from test_config import init_database


def test_user_list(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/user/list' page is requested (GET)
    THEN check the response is valid and current user list is returned
    """
    response = test_client.get('/user/list', follow_redirects=True)
    assert response.status_code == 200
    assert b"Current User List" in response.data
    assert b"test_user_admin" in response.data
    assert b"test_user_admin@gmail.com" in response.data
    assert b"test_user" in response.data
    assert b"test_user@gmail.com" in response.data


def test_user_not_found(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/user/read' page is requested (POST) and the user does not exist
    THEN check the response is a valid 200 but that the 404 error page is returned
    """
    response = test_client.get('/user/read', query_string=dict(username='unknown', email='unknown@nhs.net'),
                               follow_redirects=True)

    # Endpoint triggers a 404 which is picked up by the global error handling
    # and the 404 error page is returned (with a 200 response)
    assert response.status_code == 200
    assert b"Oops!! This page doesn't exist" in response.data


def test_user_found(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/user/read' page is requested (POST) and the user exists
    THEN check the response is valid json
    """
    response = test_client.get('/user/read', query_string=dict(username='test_user_admin',
                                                               email='test_user_admin@gmail.com'),
                               follow_redirects=True)

    json_data = json.loads(response.data)
    assert response.status_code == 200
    assert "username" in json_data
    assert "email" in json_data
    assert json_data["username"] == 'test_user_admin'
    assert json_data["email"] == 'test_user_admin@gmail.com'


def test_create_user(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/user/create' page is requested (POST)
    THEN check the response is valid and the user is in the returned list
    """
    response = test_client.post('/user/create', data=dict(username='paul.ockleford', email='paul.ockleford@nhs.net'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b"paul.ockleford" in response.data
    assert b"paul.ockleford@nhs.net" in response.data
    assert b"Current User List" in response.data


def test_delete_user(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/user/delete' page is requested (POST)
    THEN check the response is valid and that the user is not in the returned list
    """
    response = test_client.post('/user/delete',
                                data=dict(username='paul.ockleford'), follow_redirects=True)
    assert response.status_code == 200
    assert b"paul.ockleford" not in response.data
    assert b"paul.ockleford@nhs.net" not in response.data
    assert b"Current User List" in response.data


def test_update_user(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/user/update' page is requested (PUT)
    THEN check the response is valid (501) as this function is not implemented
    """
    response = test_client.put('/user/update', data=dict(username='test_user_admin'), follow_redirects=True)
    assert response.status_code == 501

