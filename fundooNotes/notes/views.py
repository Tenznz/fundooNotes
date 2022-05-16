import logging
import json

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Note, Label, Collaborator
from .serializers import NoteSerializer, LabelSerializer, CollaboratorSerializer
from .utils import verify_token
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
        serializer = NoteSerializer(data=request.data)
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
            collaborators = Collaborator.objects.filter(user_id=request.data.get('user_id'))
            note_id = list()
            for colaborator in collaborators:
                note_id.append(colaborator.note.id)
            print(note_id)
            notes = Note.objects.filter(pk__in=note_id)

            print(notes)
            return Response({
                "message": "user found",
                "data": NoteSerializer(notes, many=True).data
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
                "message": "user delete successfully"
            }, status=status.HTTP_204_NO_CONTENT)
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
            notes = Note.objects.filter(title__contains=search_data).filter(user_id=request.data.get('user_id'))|\
                    Note.objects.filter(description__contains=search_data).filter(user_id=request.data.get('user_id'))

            return Response({
                "message": "note_found",
                "data": NoteSerializer(notes, many=True).data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            logging.error(e)
            return Response({
                "error_message": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class CollaboratorAPI(APIView):
    def post(self, request):
        try:
            Collaborator.objects.create(user_id=request.data['user_id'], note_id=request.data['note_id'])
            return Response({
                "message": 'successfully',
                "data": ''
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logging.error(e)
            return Response({
                "error_message": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    @verify_token
    def get(self, request):
        """
        get note of user
        :param request:
        :return:response
        """
        try:
            col = Collaborator.objects.all()
            serializer = CollaboratorSerializer(col, many=True)

            return Response({
                "message": "user found",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "message": str(e),
            }, status=status.HTTP_400_BAD_REQUEST)
