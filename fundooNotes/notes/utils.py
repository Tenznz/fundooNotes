import logging
import json
from rest_framework.response import Response
from user.utils import EncodeDecodeToken

logging.basicConfig(filename="views.log", filemode="w")


def verify_token(function):
    def wrapper(self, request, note_id=None):
        if 'HTTP_AUTHORIZATION' not in request.META:
            resp = Response({'message': 'Authentication problem'})
            resp.status_code = 401
            logging.info('Token not provided in the header')
            return resp
        token = request.META['HTTP_AUTHORIZATION']
        id = EncodeDecodeToken.decode_token(token)
        request.data.update({'user_id': id.get("id")})
        if note_id is None:
            return function(self, request)
        else:
            return function(self, request, note_id)

    return wrapper


def get_list(rows):
    res = list()
    for row in rows:
        res.append({
            'note_id': row[0],
            'title': row[1],
            'description': row[2],
            'created_at': row[3],
            'color': row[4],
            'archive': row[5],
            'is_deleted': row[6],
            'user_id': row[7],
            'pin': row[8]
        })
    return res
