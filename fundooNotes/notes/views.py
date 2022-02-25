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

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING)
    ], operation_summary="Add notes",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'title': openapi.Schema(type=openapi.TYPE_STRING, description="title"),
                'description': openapi.Schema(type=openapi.TYPE_STRING, description="description")
            }
        ))
    @verify_token
    def post(self, request):
        """
        creating note of user
        :param request: note details
        :return:response
        """
        data = request.data
        data["user_id"] = request.data.get("id")
        # print(data)
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

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING)
    ], operation_summary="get note by user_id")
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
                })
        except Exception as e:
            return Response({
                "message": "user not found",
            })

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING)
    ], operation_summary="delete note",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'note_id': openapi.Schema(type=openapi.TYPE_INTEGER, description="note_id"),
            }
        ))
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
            })
        except Exception as e:
            logging.error(e)
            print(e)
            return Response(
                {
                    "message": "Data not deleted"
                },
                status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING)
    ], operation_summary="Update notes",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'note_id': openapi.Schema(type=openapi.TYPE_INTEGER, description="note_id"),
                'title': openapi.Schema(type=openapi.TYPE_STRING, description="title"),
                'description': openapi.Schema(type=openapi.TYPE_STRING, description="description")
            }
        ))
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
            return Response({
                "message": "user update successfully",
                "data": serializer.data
            })
        except Exception as e:
            logging.error(e)
            print(e)
            return Response(
                {
                    "message": "Data not updated"
                },
                status=status.HTTP_400_BAD_REQUEST)
