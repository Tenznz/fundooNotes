import logging

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Note
from .serializers import NoteSerializer
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from django.core.mail import send_mail
from .utils import verify_token


logging.basicConfig(filename="views.log", filemode="w")


# Create your views here.
class Notes(APIView):
    @verify_token
    def post(self, request):
        serializer = NoteSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
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
        note = Note.objects.filter(user_id_id=user_id)
        serializer = NoteSerializer(note, many=True)
        # print(repr(serializer))
        print(serializer.data)
        return Response({
            "message": "user found",
            "data": serializer.data
        })

    @verify_token
    def delete(self, request):
        try:
            note_id = request.data.get("id")
            note = Note.objects.get(id=note_id)
            note.delete()
            return Response({
                "message": "user delete successfully",
                "data": note_id
            })
        except Exception as e:
            logging.error(e)
            return Response({
                "message": "user not found"
            })

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


# def note_list(request):
#     if request.method == 'GET':
#         note = Note.objects.all()
#         serializer = NoteSerializer(note, many=True)
#         return JsonResponse(serializer.data, safe=False)
