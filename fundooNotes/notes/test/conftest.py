import pytest

from django.contrib.auth import get_user_model
from notes.models import Note


@pytest.fixture
def user_data():
    return {
        "username": "Qwert",
        "first_name": "Ten",
        "last_name": "duk",
        "password": "1234",
        "age": 26,
        "email": "duk@gmail.com",
        "phone": "1234567890",
        "is_verified": 0
    }


@pytest.fixture
def create_user(user_data):
    return get_user_model().objects.create_user(**user_data)


@pytest.fixture
def note_data():
    return {

        "title": "mynote",
        "description": "this is my notes",
        "user_id": 1
    }


@pytest.fixture
def update_note_data():
    return {
        "note_id": 1,
        "title": "my update note",
        "description": "this is my update notes",
        "user_id": 1
    }
