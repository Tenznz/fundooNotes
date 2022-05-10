import pytest
import json
from django.urls import reverse
from django.contrib.auth import get_user_model
from notes.models import Note


class TestNote:
    @pytest.mark.django_db
    def test_add_note(self, client, note_data, create_user,update_note_data):
        user_model = get_user_model()
        assert user_model.objects.count() == 1

        # add note
        url = reverse("note")
        response = client.post(url, note_data, content_type='application/json')
        assert response.status_code == 201
        user1 = user_model.objects.get(id=1)
        assert user1.id == 1

        # get note
        url = reverse('gd_note', kwargs={'id': response.data['data']['id']})
        response = client.get(url)
        assert response.data["message"] == "note found"
        assert response.status_code == 200

        # update note
        url = reverse('note')
        response = client.put(url, update_note_data, content_type='application/json')
        assert response.data['data']['title'] == update_note_data.get('title')
        assert response.status_code == 200

        # delete note
        url = reverse('gd_note', kwargs={'id': response.data['data']['id']})
        response = client.delete(url, CONTENT_TYPE='application/json')
        assert Note.objects.count() == 0
        assert response.status_code == 204
