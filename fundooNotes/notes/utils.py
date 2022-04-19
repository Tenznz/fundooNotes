import logging
import json
from rest_framework.response import Response
from user.utils import EncodeDecodeToken
from .redis import RedisCode
from .serializers import NoteSerializer

logging.basicConfig(filename="views.log", filemode="w")


def verify_token(function):
    def wrapper(self, request, note_id=None):
        print(request.META)
        if 'HTTP_AUTHORIZATION' not in request.META:
            resp = Response({'message': 'Token not provided in the header'})
            resp.status_code = 401
            logging.info('Token not provided in the header')
            return resp
        token = request.META['HTTP_AUTHORIZATION']
        id = EncodeDecodeToken.decode_token(token)
        request.data.update({'id': id.get("id")})
        if note_id is None:
            return function(self, request)
        else:
            return function(self, request, note_id)

    return wrapper


def get_note_format(note_data):
    note_list = []
    for note in note_data:
        note_labels = note.label_set.all()
        print(note_labels)
        note_list.append({
            "note_id": note.id,
            "title": note.title,
            "description": note.description,
            "created_at": note.created_at,
            "color": note.color,
            "archive": note.archive,
            "is_deleted": note.is_deleted,
            "label_list": [label.get_label() for label in note_labels]
        })

    return note_list
