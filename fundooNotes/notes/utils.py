import logging
from rest_framework.response import Response
from user.utils import EncodeDecodeToken

logging.basicConfig(filename="views.log", filemode="w")


def verify_token(function):
    def wrapper(self, request):
        # print(request.META)
        if 'HTTP_AUTHORIZATION' not in request.META:
            resp = JsonResponse({'message': 'Token not provided in the header'})
            resp.status_code = 400
            logger.info('Token not provided in the header')
            return resp
        token = request.META['HTTP_AUTHORIZATION']
        encode = token.split(" ")
        # print(encode[1])
        id = EncodeDecodeToken.decode_token(encode[1])
        request.data.update({'id': id.get("id")})
        return function(self, request)

    return wrapper
