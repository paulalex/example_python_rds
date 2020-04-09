"""
This file contains unit tests for the User model
"""

from test_config import non_admin_user
from test_config import admin_user


def test_new_non_admin_user(non_admin_user):
    """
    GIVEN a User model
    WHEN I create a new user
    THEN the user is created and is NOT an administrator
    """
    assert non_admin_user.username == 'Test User'
    assert non_admin_user.email == 'test_user@gmail.com'
    assert non_admin_user.created == '2019-11-07 23:37:57.373846'
    assert not non_admin_user.admin


def test_new_admin_user(admin_user):
    """
    GIVEN a User model
    WHEN I create a new user
    THEN the user is created and IS an administrator
    """
    assert admin_user.username == 'Test User Admin'
    assert admin_user.email == 'test_user_admin@gmail.com'
    assert admin_user.created == '2019-11-07 23:38:57.373846'
    assert admin_user.admin
