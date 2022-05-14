import logging
import json

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Note
from .serializers import NoteSerializer
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from .utils import verify_token

logging.basicConfig(filename="views.log", filemode="w")


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
                }, 201)
        except ValidationError as e:
            logging.error(e)
            return Response({
                'message': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logging.error(e)
            return Response({
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    @verify_token
    def get(self, request):
        try:
            note = Note.objects.filter(user_id_id=request.data.get("user_id"))
            serializer = NoteSerializer(note, many=True)
            return Response({
                "message": "user found",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({
                "message": "note not found"
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "message": str(e),
            }, status=status.HTTP_400_BAD_REQUEST)

    @verify_token
    def delete(self, request, pk):
        try:
            Note.objects.get(pk=pk).delete()
            return Response({
                "message": "note delete successfully"
            }, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            return Response({
                "message": "note not found"
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logging.error(e)
            print(e)
            return Response(
                {
                    "message": "Data not deleted"
                }, status=status.HTTP_400_BAD_REQUEST)

    @verify_token
    def put(self, request):
        try:
            note = Note.objects.get(pk=request.data["note_id"])
            serializer = NoteSerializer(note, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({
                "message": "user update successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({
                "message": "note not found"
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logging.error(e)
            return Response(
                {
                    "message": "Data not updated"
                }, status=status.HTTP_400_BAD_REQUEST)
