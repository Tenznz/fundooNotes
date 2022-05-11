import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from notes.models import Note


class TestNote:
    @pytest.mark.django_db
    def test_add_note(self, client, note_data, user_data, create_user, update_note_data):
        user_model = get_user_model()
        assert user_model.objects.count() == 1
        url = reverse("login")
        response = client.post(url, user_data)
        assert response.status_code == 200
        token = response.data['token']

        # add note
        url = reverse("note")
        response = client.post(url, note_data, content_type='application/json', HTTP_AUTHORIZATION=token)
        assert response.status_code == 201
        user1 = user_model.objects.get(id=1)
        assert user1.id == 1

        # get note
        url = reverse('note')
        response = client.get(url, HTTP_AUTHORIZATION=token)
        assert response.data["message"] == "note found"
        assert response.status_code == 200
        note_id = response.data['data'][0]['id']

        # update note
        url = reverse('note')
        response = client.put(url, update_note_data, content_type='application/json', HTTP_AUTHORIZATION=token)
        assert response.status_code == 200

        # delete note
        url = reverse('note_delete', kwargs={'pk': note_id})
        response = client.delete(url, CONTENT_TYPE='application/json', HTTP_AUTHORIZATION=token)
        assert Note.objects.count() == 0
        assert response.status_code == 204