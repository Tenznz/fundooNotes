import logging

from django.core.exceptions import ObjectDoesNotExist
from django.db import connection
from django.db.models import Q
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from user.models import User
from .models import Note, Label
from .serializers import NoteSerializer, LabelSerializer
from .utils import verify_token, get_list

logging.basicConfig(filename="views.log", filemode="w")

cursor = connection.cursor()


class Notes(APIView):
    """ class based views for curd operation of user note """

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
        except ValidationError as e:
            logging.error(e)
            return Response({
                'message': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
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
        # # print(dir(cursor))
        # cursor.execute('SELECT * FROM notes_note AS note JOIN user_user ON note.id = user_user.id WHERE user_user.id '
        #                '= %s', [request.data['user_id']])


        # for i in rows:
        #     print(i[2])
        try:
            # user = User.objects.get(id=request.data['user_id'])
            # notes = user.collaborator.all() | Note.objects.filter(user_id=request.data['user_id'])
            cursor.execute('SELECT note.id,note.title,note.description,note.created_at,note.color,note.archive,'
                           'note.is_deleted,note.user_id_id,note.pin as note_id FROM notes_note AS note LEFT JOIN '
                           'notes_note_collaborator AS cola ON note.id=cola.note_id WHERE note.user_id_id=%s or '
                           'cola.user_id=%s;', [request.data['user_id'], request.data['user_id']])

            rows = cursor.fetchall()

            return Response({
                "message": "note found",
                "data": get_list(rows)
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "message": str(e),
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
            note.delete()
            return Response({
                "message": "note delete successfully"
            }, status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            return Response(
                {
                    "message": 'note not found'
                },
                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logging.error(e)
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
            note = Note.objects.get(pk=request.data["note_id"])
            serializer = NoteSerializer(note, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                {
                    "message": "note update successfully",
                    "data": serializer.data
                },
                status=status.HTTP_204_NO_CONTENT
            )
        except ObjectDoesNotExist:
            return Response(
                {
                    "message": 'note not found'
                },
                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logging.error(e)
            print(e)
            return Response(
                {
                    "error_message": str(e)
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
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            logging.error(e)
            return Response({
                "error_message": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        try:
            label_data = Label.objects.all()
            return Response({
                'message': 'labels retrieve successfully',
                "notes list": LabelSerializer(label_data, many=True).data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logging.error(e)
            return Response({
                "error_message": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        try:
            label = Label.objects.get(name=request.data.get("label_name"))
            label.delete()
            return Response({
                "message": "label delete successfully"
            }, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            logging.error(e)
            return Response({
                "error_message": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class SearchAPI(APIView):
    @verify_token
    def get(self, request):
        try:
            search_data = request.data.get('search')
            notes = Note.objects.filter(Q(title__contains=search_data) |
                                        Q(description__contains=search_data),
                                        user_id=request.data['user_id'])
            return Response({
                "message": "note_found",
                "data": NoteSerializer(notes, many=True).data
            }, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            return Response(
                {
                    "message": 'note not found'
                },
                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logging.error(e)
            return Response({
                "error_message": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class CollaboratorAPI(APIView):
    def post(self, request):
        try:
            note = Note.objects.get(id=request.data['note_id'], user_id=request.data['user_id'])
            user = User.objects.get(id=request.data['collaborator_id'])
            user.collaborator.add(note)
            return Response({
                "message": 'successfully',
                "data": ''
            }, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(
                {
                    "message": 'note not found'
                },
                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logging.error(e)
            return Response({
                "error_message": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    #
    @verify_token
    def get(self, request):
        """
        get note of user
        :param request:
        :return:response
        """
        try:
            user = User.objects.get(id=request.data['user_id'])
            note = user.collaborator.all() | Note.objects.filter(user_id=request.data['user_id'])
            print([i for i in note])
            return Response({
                "message": "user found",
                "data": NoteSerializer(note, many=True).data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "message": str(e),
            }, status=status.HTTP_400_BAD_REQUEST)
