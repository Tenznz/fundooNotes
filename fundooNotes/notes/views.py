import logging

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Note
from .serializers import NoteSerializer
from django.http import JsonResponse
from rest_framework.parsers import JSONParser

logging.basicConfig(filename="views.log", filemode="w")


# Create your views here.
class Notes(APIView):
    def post(self, request):
        data = JSONParser().parse(request)
        serializer = NoteSerializer(data=data)
        try:

            if serializer.is_valid(raise_exception=True):
                serializer.save()
            return Response(
                {
                    "message": "Data store successfully",
                    "data": serializer.data
                })
        except Exception as e:
            logging.error(e)
            return Response(serializer.errors)

    def get(self, request):

        note = Note.objects.all()
        serializer = NoteSerializer(note, many=True)
        return JsonResponse(serializer.data, safe=False)
