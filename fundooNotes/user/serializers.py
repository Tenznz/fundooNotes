from rest_framework import serializers
from user.models import User


class UserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=200)
    first_name = serializers.CharField(max_length=200)
    last_name = serializers.CharField(max_length=200)
    password = serializers.CharField(max_length=50)
    age = serializers.IntegerField()
    email = serializers.EmailField(max_length=40)
    phone = serializers.CharField(max_length=10)
    is_verified = serializers.BooleanField(default=False)

    def create(self, validated_data):
        """
        Create and return a new `User` instance, given the validated data.
        """
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `User` instance, given the validated data.
        """
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.password = validated_data.get('password', instance.password)
        instance.email = validated_data.get('email', instance.email)
        instance.age = validated_data.get('age', instance.age)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.is_verified = validated_data.get('is_verified', instance.is_verified)

        instance.save()
        return instance
