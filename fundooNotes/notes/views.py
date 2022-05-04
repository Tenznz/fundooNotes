import logging

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from .models import Note
from .serializers import NoteSerializer

logging.basicConfig(filename="views.log", filemode="w")


# Create your views here.
class Notes(APIView):
    def post(self, request):
        serializer = NoteSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                {
                    "message": "Data store successfully",
                    "data": serializer.data
                }, 201)
        except ValidationError:
            return Response({
                'message': serializer.errors
            }, 400)

        except Exception as e:
            logging.error(e)
            return Response({'message': str(e)}, 400)

    def get(self, request):
        try:
            note = Note.objects.filter(user_id_id=request.data.get("user_id"))
            serializer = NoteSerializer(note, many=True)
            return Response({
                "message": "note found",
                "data": serializer.data
            }, 200)
        except Exception as e:
            return Response({
                'message': str(e)
            }, 400)

    def delete(self, request):
        try:
            Note.objects.get(id=request.data.get("note_id")).delete()
            return Response({
                "message": "note delete successfully",
            }, 204)
        except ObjectDoesNotExist:
            return Response({
                'message': 'note not found'
            }, 400)
        except Exception as e:
            logging.error(e)
            return Response({
                "message": "note not found"
            }, 400)

    def put(self, request):
        note = Note.objects.get(pk=request.data["note_id"])
        serializer = NoteSerializer(note, data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({
                "message": "user update successfully",
                "data": serializer.data
            }, 200)
        except ValidationError:
            return Response({
                'message': serializer.errors
            }, 400)
        except Exception as e:
            logging.error(e)
            Response({
                'message': str(e)
            }, 400)
