import logging
import json

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Note
from .serializers import NoteSerializer
from .utils import verify_token
from django.db import connection
from datetime import datetime
from user.utils import dictfetchall

cursor = connection.cursor()

logging.basicConfig(filename="views.log", filemode="w")


class Notes(APIView):
    """ class based views for curd operation of user note """

    @verify_token
    def post(self, request):
        """
        creating note of user
        :param request: note details
        :return:response
        """
        try:

            cursor.execute(
                "insert into notes_note (title,description,created_at,user_id_id) values(%s,%s,%s,%s)",
                [request.data['title'], request.data['description'], datetime.now(),
                 request.data['user_id']])
            return Response(
                {
                    "message": "Data store successfully",
                }, status=status.HTTP_201_CREATED)
        except Exception as e:
            logging.error(e)
            return Response(
                {
                    "message": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST)

    @verify_token
    def get(self, request):
        """
        get note of user
        :param request:
        :return:response
        """
        try:
            note = Note.objects.raw(f"select * from notes_note where user_id_id={request.data['user_id']}")
            serializer = NoteSerializer(note, many=True)
            return Response({
                "message": "note found",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "message": "note not found",
            }, status=status.HTTP_400_BAD_REQUEST)

    @verify_token
    def delete(self, request, pk):
        """
        delete note of user
        :param request: note_id
        :return:response
        """
        try:
            cursor.execute('delete from notes_note where id=%s', [pk])
            return Response({
                "message": "user delete successfully"
            }, 204)
        except Exception as e:
            logging.error(e)
            print(e)
            return Response(
                {
                    "message": "Data not deleted"
                },
                status=status.HTTP_400_BAD_REQUEST)

    @verify_token
    def put(self, request):
        """
        update note of user
        :param request: note id
        :return:response 
        """
        try:
            cursor.execute("update notes_note set title=%s,description=%s where id=%s",
                           [request.data.get('title'),
                            request.data.get('description'),
                            request.data.get('note_id')])

            return Response(
                {
                    "message": "user update successfully",
                    # "data": serializer.data
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            logging.error(e)
            print(e)
            return Response(
                {
                    "message": "Data not updated"
                },
                status=status.HTTP_400_BAD_REQUEST)
