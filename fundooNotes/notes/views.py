import logging

from django.core.exceptions import ObjectDoesNotExist
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Note
from .serializers import NoteSerializer
from .utils import verify_token

logging.basicConfig(filename="views.log", filemode="w")


class Notes(APIView):
    """ class based views for curd operation of user note """

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('AUTHORIZATION', openapi.IN_HEADER, type=openapi.TYPE_STRING)
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
        serializer = NoteSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                {
                    "message": "note added successfully",
                    "data": serializer.data
                }, status=status.HTTP_201_CREATED)
        except Exception as e:
            logging.error(e)
            return Response(
                {
                    "message": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('AUTHORIZATION', openapi.IN_HEADER, type=openapi.TYPE_STRING)
    ], operation_summary="get note by user_id")
    @verify_token
    def get(self, request):
        """
        get note of user
        :param request:
        :return:response
        """
        try:
            note = Note.objects.filter(user_id_id=request.data.get("user_id"))
            serializer = NoteSerializer(note, many=True)
            return Response({
                "message": "note found",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "message": str(e),
            }, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('AUTHORIZATION', openapi.IN_HEADER, type=openapi.TYPE_STRING)
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
            note = Note.objects.get(pk=request.data["note_id"])
            serializer = NoteSerializer(note, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                {
                    "message": "note update successfully",
                    "data": serializer.data
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            logging.error(e)
            return Response(
                {
                    "message": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST)


class NoteDelete(APIView):
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('AUTHORIZATION', openapi.IN_HEADER, type=openapi.TYPE_STRING)
    ], operation_summary="delete note",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'note_id': openapi.Schema(type=openapi.TYPE_INTEGER, description="note_id"),
            }
        ))
    @verify_token
    def delete(self, request, pk):
        """
        delete note of user
        :param request: note_id
        :return:response
        """
        try:
            Note.objects.get(pk=pk).delete()

            return Response({
                "message": "note delete successfully"
            }, 204)
        except ObjectDoesNotExist:
            return Response({
                'message': 'note not found'
            }, 400)
        except Exception as e:
            logging.error(e)
            return Response(
                {
                    "message": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST)
