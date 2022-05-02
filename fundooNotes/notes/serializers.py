from rest_framework import serializers
from .models import Note
from user.models import User


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['title', 'description', 'user_id']

    # def create(self, validated_data):
    #     """
    #     Create and return a new `Snippet` instance, given the validated data.
    #
    #     """
    #     try:
    #         note = Note(
    #             title=validated_data.get('title'),
    #             description=validated_data.get('description'),
    #             user_id=validated_data.get('user_id')
    #         )
    #         return note
    #     except Exception as e:
    #         print(e)

    # def create_new_note(self, validated_data):
    #     return Note.objects.create(**validated_data)

    # def update(self, instance, validated_data):
    #     """
    #     Update and return an existing `Snippet` instance, given the validated data.
    #     """
    #     instance.title = validated_data.get('title', instance.title)
    #     instance.description = validated_data.get('description', instance.description)
    #     instance.created_at = validated_data.get('created_at', instance.created_at)
    #     instance.user_id = validated_data.get('user_id', instance.user_id)
    #     instance.save()
    #
    #     return instance
