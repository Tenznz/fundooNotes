import logging

from notes.models import Note
from notes.serializers import NoteSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import permissions
from notes.permission import IsUser
from .utils import verify_token
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

logging.basicConfig(filename="views.log", filemode="w")


class NoteList(ListCreateAPIView):
    serializer_class = NoteSerializer
    queryset = Note.objects.all()
    permission = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        return serializer.save(id=self.request.data)

    def get_queryset(self):
        return self.queryset.filter(user_id=self.request.data.get("user_id"))


class NotesDetails(RetrieveUpdateDestroyAPIView):
    serializer_class = NoteSerializer
    queryset = Note.objects.all()
    permission = (permissions.IsAuthenticated, IsUser)
    lookup_field = "id"

    def perform_create(self, serializer):
        return serializer.save(id=self.request.data)

    def get_queryset(self):
        return self.queryset.filter(id=self.request.data["id"])
