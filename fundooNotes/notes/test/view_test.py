import pytest
from rest_framework.reverse import reverse
from notes.serializers import NoteSerializer

pytestmark = pytest.mark.django_db


class TestNote:
    @pytest.mark.django_db
    def test_note_fail(self, client):
        url = reverse("note")
        note = {
            "title": "Ten",
            "description": "Science fiction animation"
        }
        print(url)
        response = client.post(path=url, data=note,content_type="application/json",
                               HTTP_AUTHORIZATION='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MX0'
                                                  '.-xXA0iKB4mVNvWLYFtt2xNiYkFpObF54J9lj2RwduAI')
        print(response.content)
        assert response.status_code == 400
