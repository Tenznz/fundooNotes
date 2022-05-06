import pytest
import json
from django.urls import reverse
from django.contrib.auth import get_user_model
from notes.models import Note


class TestNote:
    @pytest.mark.django_db
    def test_add_note(self, client, note_data, create_user):
        user_model = get_user_model()
        assert user_model.objects.count() == 1
        user1 = user_model.objects.get(id=1)
        assert user1.id == 1
        url = reverse("note")
        response = client.post(url, note_data)
        print(response.content)
        assert response.status_code == 201

    @pytest.mark.django_db
    def test_get_note_empty(self, client):
        url = reverse('gd_note', kwargs={'id': 0})
        response = client.get(url)
        assert response.data["message"] == "empty note"
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_get_note(self, client, create_note, note_data, user_id):
        user_model = get_user_model()
        user = user_model.objects.get(id="2")
        assert len(Note.objects.filter(user_id_id=2)) == 1
        url = reverse('gd_note', kwargs={'id': user.id})
        response = client.get(path=url)
        assert response.data["message"] == "note found"
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_delete_note(self, client, create_note):
        assert Note.objects.count() == 1
        note = Note.objects.get(id=3)
        assert note.id == 3
        url = reverse('gd_note', kwargs={'id': note.id})
        response = client.delete(url, CONTENT_TYPE='application/json')
        assert Note.objects.count() == 0
        assert response.status_code == 204

    @pytest.mark.django_db
    def test_update_note(self, client, create_note):
        notes = Note.objects.all()
        assert len(notes) == 1
        url = reverse('note')

        update_note = {
            "note_id": notes[0].id,
            "title": "my update note",
            "description": "this is my update notes",
            "user_id": notes[0].user_id_id
        }
        response = client.put(url, json.dumps(update_note), content_type='application/json')
        assert response.data['data']['title'] == update_note.get('title')
        assert response.status_code == 200
