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


class RedisOperation:

    def __init__(self):
        self.redis_obj = RedisCode()

    def get_note(self, user_id):
        """
        for geting note from cache
        :param user_id: user_id
        :return:
        """
        print("data from redis server")
        try:
            data = self.redis_obj.get(user_id)
            if data is None:
                return None
            return json.loads(data)
        except Exception as e:
            logging.error(e)
            raise e

    def add_note(self, user_id, note):
        """
        Adding note to cache
        :param user_id: user_id
        :param note: note details
        :return:
        """
        try:
            print("data added to redis server")
            existing_note = self.get_note(user_id)
            if existing_note is None:
                note_data = {int(note.get('id')): note}
            else:
                new_note = {int(note.get('id')): note}
                note_data = {**existing_note, **new_note}
            self.redis_obj.set(user_id, json.dumps(note_data))
        except Exception as e:
            logging.error(e)

    def delete_note(self, user_id, note_id):
        """
        deleting note to cache
        :param user_id:
        :param note_id:
        :return:
        """

        print("data delete to redis server")
        try:
            note_list = json.loads(self.redis_obj.get(user_id))
            if note_list.get(str(note_id)):
                note_list.pop(str(note_id))
                self.redis_obj.set(user_id, json.dumps(note_list))
        except Exception as e:
            logging.error(e)

    def update_note(self, note):
        """
        deleting note to cache
        :param note:note details
        :return:
        """
        try:
            user_id = note.get('user_id')
            id = str(note.get("id"))
            note_dict = json.loads(self.redis_obj.get(user_id))

            if note_dict.get(id):
                note_dict.update({id: note})
                self.redis_obj.set(user_id, json.dumps(note_dict))
            else:
                print("id not found")

        except Exception as e:
            logging.error(e)
