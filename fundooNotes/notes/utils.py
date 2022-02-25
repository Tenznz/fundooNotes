import logging
import json
from rest_framework.response import Response
from user.utils import EncodeDecodeToken
from .redis import RedisCode
from .serializers import NoteSerializer

logging.basicConfig(filename="views.log", filemode="w")


def verify_token(function):
    def wrapper(self, request):
        print(request.META)
        if 'HTTP_TOKEN' not in request.META:
            resp = Response({'message': 'Token not provided in the header'})
            resp.status_code = 400
            logging.info('Token not provided in the header')
            return resp
        token = request.META['HTTP_TOKEN']
        id = EncodeDecodeToken.decode_token(token)
        request.data.update({'id': id.get("id")})
        return function(self, request)

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
            dict_data = {user_id: existing_note}
            if existing_note is None:
                new_note = {int(note.get('id')): note}

                dict_data[user_id] = new_note
                self.redis_obj.set(user_id, json.dumps(dict_data[user_id]))
            else:
                new_note = {int(note.get('id')): note}
                added_note = {**existing_note, **new_note}
                self.redis_obj.set(user_id, json.dumps(added_note))
        except Exception as e:
            logging.error(e)
            raise e

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
                self.redis_obj.put(user_id, json.dumps(note_list))
        except Exception as e:
            logging.error(e)
            raise e

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
