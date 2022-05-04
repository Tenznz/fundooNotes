import pytest
from rest_framework.reverse import reverse
from notes.serializers import NoteSerializer

pytestmark = pytest.mark.django_db


class TestNote:
    @pytest.mark.django_db
    def test_add_note(self, client):
        url = reverse("note")
        note = {
            "title": "mynote",
            "description": "this is my notes",
            "user_id": 264
        }
        response = client.post(url, note)
        print(response.content)
        assert response.status_code == 201

    @pytest.mark.django_db
    def test_get_note(self, client):
        url = reverse("note")
        note = {
            "note_id": 4,
        }
        print(url)
        response = client.get(url, note)
        print(response.content)
        assert response.status_code == 200
