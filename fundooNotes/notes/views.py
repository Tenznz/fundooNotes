import logging
import json

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Note
from .serializers import NoteSerializer
from django.http import JsonResponse
from django.core.mail import send_mail
from .utils import verify_token, RedisOperation

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
        data = request.data
        data["user_id"] = request.data.get("id")
        serializer = NoteSerializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            RedisOperation().add_note(request.data.get("id"), note=serializer.data)
            return Response(
                {
                    "message": "Data store successfully",
                    "data": serializer.data
                }, status=status.HTTP_201_CREATED)
        except Exception as e:
            logging.error(e)
            return Response(
                {
                    "message": "Data not stored"
                },
                status=status.HTTP_400_BAD_REQUEST)

    @verify_token
    def get(self, request):
        """
        get note of user
        :param request:
        :return:response
        """
        user_id = request.data.get("id")
        try:
            data = RedisOperation().get_note(user_id=user_id).values()
            if data is not None:
                return Response({
                    "message": "user found",
                    "data": data
                })
            else:
                print("data from db")
                note = Note.objects.filter(user_id_id=user_id)
                serializer = NoteSerializer(note, many=True)
                print(serializer.data)
                return Response({
                    "message": "user found",
                    "data": serializer.data
                },status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "message": "user not found",
            },status=status.HTTP_400_BAD_REQUEST)

    @verify_token
    def delete(self, request):
        """
        delete note of user
        :param request: note_id
        :return:response
        """
        try:
            note = Note.objects.get(pk=request.data["note_id"])
            print(note)
            RedisOperation().delete_note(request.data.get("id"), request.data.get("note_id"))
            note.delete()
            return Response({
                "message": "user delete successfully"
            },status=status.HTTP_201_CREATED)
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
            data = request.data
            data["user_id"] = request.data.get("id")
            note = Note.objects.get(pk=request.data["note_id"])
            print(note)
            serializer = NoteSerializer(note, data=data)

            serializer.is_valid(raise_exception=True)
            serializer.save()
            RedisOperation().update_note(serializer.data)
            return Response(
                {
                    "message": "user update successfully",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            logging.error(e)
            print(e)
            return Response(
                {
                    "message": "Data not updated"
                },
                status=status.HTTP_400_BAD_REQUEST)
