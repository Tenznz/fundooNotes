from rest_framework import serializers
from user.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'password', 'age', 'email', 'phone', 'is_verified']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
