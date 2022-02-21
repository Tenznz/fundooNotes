import logging
import json
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Note
from .serializers import NoteSerializer
from django.http import JsonResponse
from django.core.mail import send_mail
from .utils import verify_token, RedisOperation

logging.basicConfig(filename="views.log", filemode="w")


# Create your views here.
class Notes(APIView):
    @verify_token
    def post(self, request):
        serializer = NoteSerializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            RedisOperation().add_note(note=serializer.data)
            return Response(
                {
                    "message": "Data store successfully",
                    "data": serializer.data
                })
        except Exception as e:
            logging.error(e)
            return Response(serializer.errors)

    @verify_token
    def get(self, request):
        user_id = request.data.get("user_id")
        try:
            data = RedisOperation().get_note(user_id=user_id)
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

    @verify_token
    def delete(self, request):
        try:
            note = Note.objects.get(pk=request.data["note_id"])
            print(note)
            RedisOperation().delete_note(request.data.get("user_id"), request.data.get("note_id"))
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

    #

    @verify_token
    def put(self, request):
        note = Note.objects.get(pk=request.data["id"])
        print(note)
        serializer = NoteSerializer(note, data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({
                "message": "user update successfully",
                "data": serializer.data
            })
        except Exception as e:
            logging.error(e)
            print(e)
            Response(serializer.errors)
