import pytest
from rest_framework.reverse import reverse
from notes.serializers import NoteSerializer

pytestmark = pytest.mark.django_db


class TestNote:
    @pytest.mark.django_db
    def test_user(self, client):
        url = reverse("note")
        note = {
            "title": "Ten",
            "description": "Science fiction animation",
            # "user_id_id": 4
        }
        print(url)
        response = client.post(url, note)
        print(response.content)
        assert response.status_code == 200

    # @pytest.mark.django_db
    # def update(self):
    #     = reverse("note")

