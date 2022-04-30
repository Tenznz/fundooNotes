import logging
import json
from rest_framework.response import Response
from user.utils import EncodeDecodeToken
from .serializers import NoteSerializer

logging.basicConfig(filename="views.log", filemode="w")


def verify_token(function):
    def wrapper(self, request, note_id=None):
        if 'HTTP_AUTHORIZATION' not in request.META:
            resp = Response({'message': 'Token not provided in the header'})
            resp.status_code = 401
            logging.info('Token not provided in the header')
            return resp
        token = request.META['HTTP_AUTHORIZATION']
        id = EncodeDecodeToken.decode_token(token)
        request.data.update({'id': id.get("id")})
        if note_id:
            return function(self, request, note_id)
        return function(self, request)

    return wrapper
