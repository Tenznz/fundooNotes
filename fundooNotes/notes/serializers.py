from rest_framework import serializers
from notes.models import Note, Label


class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ['id', 'name', 'color']


class NoteSerializer(serializers.ModelSerializer):
    """ Serializer is used to converting the python object """

    label = serializers.SerializerMethodField()

    class Meta:
        model = Note
        fields = ['id', 'title', 'description', 'user_id', 'label']
        read_only_fields = ['label']  # post,put

    def get_label(self, obj):
        try:
            note_labels = obj.label_set.all()
            label = LabelSerializer(note_labels, many=True)
            return label.data
        except obj.DoesNotExist:
            return []
