import logging
import json
from rest_framework.response import Response
from user.utils import EncodeDecodeToken
from .serializers import NoteSerializer

logging.basicConfig(filename="views.log", filemode="w")


def verify_token(function):
    def wrapper(self, request, *args, **kwargs):
        # print(request.META)
        if 'HTTP_AUTHORIZATION' not in request.META:
            resp = Response({'message': 'Token not provided in the header'})
            resp.status_code = 400
            logging.info('Token not provided in the header')
            return resp
        token = request.META['HTTP_AUTHORIZATION']
        id = EncodeDecodeToken.decode_token(token)
        request.data.update({'user_id': id.get("id")})
        return function(self, request, *args, **kwargs)

    return wrapper
