import logging
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Note
from .serializers import NoteSerializer
from .utils import verify_token

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
        get notes of user
        :param request:
        :return:response
        """
        try:
            note = Note.objects.filter(user_id=request.data.get("user_id"))
            serializer = NoteSerializer(note, many=True)
            return Response({
                "message": "note found",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "message": str(e),
            }, status=status.HTTP_400_BAD_REQUEST)

    @verify_token
    def delete(self, request, pk):
        """
        delete note of user
        :param request:
        :param pk: note_id
        :return:response
        """
        try:
            note = Note.objects.get(pk=pk)
            note.delete()
            return Response({
                "message": "user delete successfully"
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            logging.error(e)
            print(e)
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
            print(note)
            serializer = NoteSerializer(note, data=request.data)

            serializer.is_valid(raise_exception=True)
            serializer.save()
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
                    "message": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST)
