from rest_framework import serializers
from .models import Note


class NoteSerializer(serializers.Serializer):
    user_id_id = serializers.IntegerField()
    created_at = serializers.DateTimeField()
    title = serializers.CharField()
    description = serializers.CharField()

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Note.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.created_at = validated_data.get('created_at', instance.created_at)
        instance.user_id = validated_data.get('user_id', instance.user_id)
        instance.save()

        return instance
