import logging
import json
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
# import RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from django.http import JsonResponse
from .models import Note, Label
from .serializers import NoteSerializer
from django.http import JsonResponse
from django.core.mail import send_mail
from .utils import verify_token, RedisOperation
from rest_framework.exceptions import ValidationError

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
            return Response(
                {
                    "message": "Data store successfully",
                    "data": serializer.data
                }, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            logging.error(e)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except NameError as e:
            logging.error(e)
            return Response({
                "message": "nameError"
            }, status=status.HTTP_400_BAD_REQUEST)

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
            note = Note.objects.filter(user_id=user_id).order_by("-id")
            serializer = NoteSerializer(note, many=True)
            print(type(serializer.data))
            return Response({
                "message": "user found",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "message": "user not found",
            }, status=status.HTTP_400_BAD_REQUEST)

    @verify_token
    def delete(self, request, note_id):
        """
            delete note of user
            :param note_id: note_id
            :param request:
            :return:response
            """
        try:
            note = Note.objects.get(pk=note_id)
            print(note)
            note.delete()
            return Response({
                "message": "user delete successfully"
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            logging.error(e)
            print("reach Exception")
            return Response(
                {
                    "message": str(e)
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
            return Response(
                {
                    "message": "user update successfully",
                    "data": serializer.data
                },
                status=status.HTTP_204_NO_CONTENT
            )
        except Exception as e:
            logging.error(e)
            print(e)
            return Response(
                {
                    "message": "Data not updated"
                },
                status=status.HTTP_400_BAD_REQUEST)


class Labels(APIView):
    """label to the notes"""

    def post(self, request):
        try:
            request_data = request.data
            note_id = request_data.get('note_id')
            label = Label.objects.filter(name=request.data.get('label_name'))
            if len(label) == 1:
                label = Label.objects.get(name=request.data.get('label_name'))
            else:
                label = Label(name=request.data.get('label_name'), color=request.data.get('color'))
                label.save()
                print(label)
            label.note.add(note_id)
            return Response({
                "message": "label added successfully"
            })
        except Exception as e:
            logging.error(e)
            return Response({
                "error_message": str(e)
            })

    def get(self, request):
        try:
            request_data = request.data
            label_name = request_data.get("label_name")
            label_data = Label.objects.get(name=label_name)
            note_data = label_data.note.all()
            return Response({
                "label_name": label_name,
                "notes list": [x.get_format() for x in note_data]
            })
        except Exception as e:
            logging.error(e)
            return Response({
                "error_message": str(e)
            })

    def delete(self, request):
        request_data = request.data
        label = Label.objects.get(name=request_data.get("label_name"))
        label.delete()
        return Response({
            "message": "label delete successfully"
        })
