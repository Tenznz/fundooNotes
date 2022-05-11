from rest_framework import serializers
from .models import Note


class NoteSerializer(serializers.ModelSerializer):
    """ Serializer is used to converting the python object """
    class Meta:
        model = Note
        fields = "__all__"



