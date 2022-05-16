from rest_framework import serializers
from notes.models import Note, Label, Collaborator
from user.serializers import UserSerializer
from user.models import  User


class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ['id', 'name', 'color']


class NoteSerializer(serializers.ModelSerializer):
    """ Serializer is used to converting the python object """

    label = serializers.SerializerMethodField()

    class Meta:
        model = Note
        fields = ['id', 'title', 'description', 'color', 'label']
        read_only_fields = ['label']  # post,put

    def get_label(self, obj):
        try:
            note_labels = obj.label_set.all()
            print(obj)
            label = LabelSerializer(note_labels, many=True)
            return label.data
        except obj.DoesNotExist:
            return []

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
            color=validate_data.get("color"),
        )
        print("notes")
        return notes


class CollaboratorSerializer(serializers.ModelSerializer):
    notes = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    class Meta:
        model = Collaborator
        fields = ['id', 'notes', 'user']

    def get_user(self, obj):
        user = User.objects.get(id=obj.user.id)
        return UserSerializer(user).data

    def get_notes(self, obj):
        notes = Note.objects.filter(id=obj.note.id)
        return NoteSerializer(notes, many=True).data
