import logging
from rest_framework.response import Response
from user.utils import EncodeDecodeToken

logging.basicConfig(filename="views.log", filemode="w")


def verify_token(function):
    def wrapper(self, request, pk=None):
        if 'HTTP_AUTHORIZATION' not in request.META:
            resp = Response({'message': 'Token not provided in the header'})
            resp.status_code = 400
            logging.info('Token not provided in the header')
            return resp
        token = request.META['HTTP_AUTHORIZATION']
        id = EncodeDecodeToken.decode_token(token)
        request.data.update({'user_id': id.get("id")})
        if pk is not None:
            return function(self, request, pk)
        return function(self, request)

    return wrapper
