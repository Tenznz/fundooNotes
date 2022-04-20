from rest_framework import serializers
from notes.models import Note, Label


class NoteSerializer(serializers.ModelSerializer):
    """ Serializer is used to converting the python object """

    class Meta:
        model = Note
        fields = "__all__"

    def create(self, validate_data):
        """
        for creating the user
        :param validate_data: validating the api data
        :return:notes
        """
        notes = Note.objects.create(
            title=validate_data.get("title"),
            description=validate_data.get("description"),
            user_id=validate_data.get("user_id"),
            # created_at=validate_data.get("created_at"),
            color=validate_data.get("color"),
            # archive=validate_data.get("archive"),
            # is_deleted=validate_data.get("is_deleted")
        )
        print("notes")
        return notes


class LabelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Label
        fields = ['id','name','color']
