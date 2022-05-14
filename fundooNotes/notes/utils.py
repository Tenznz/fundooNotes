import logging
import json
from rest_framework.response import Response
from user.utils import EncodeDecodeToken
from .redis import RedisCode
from .serializers import NoteSerializer

logging.basicConfig(filename="views.log", filemode="w")


def verify_token(function):
    def wrapper(self, request, *args, **kwargs):
        if 'HTTP_AUTHORIZATION' not in request.META:
            resp = Response({'message': 'Authentication problem'})
            resp.status_code = 400
            return resp
        token = request.META['HTTP_AUTHORIZATION']
        id = EncodeDecodeToken.decode_token(token)
        request.data.update({'user_id': id.get("id")})
        return function(self, request, *args, **kwargs)

    return wrapper
