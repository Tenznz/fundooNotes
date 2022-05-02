from rest_framework import serializers
from user.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'password', 'age', 'email', 'phone', 'is_verified']
        read_only_fields = ['id', 'is_verified']
        extra_kwargs = {'password': {'write_only': True}}

    # def create(self, validated_data):
    #     """
    #     Create and return a new `User` instance, given the validated data.
    #     """
    #     return User.objects.create_user(**validated_data)

    def create(self, validated_data):
        password = validated_data.pop('password')
        instance = self.Meta.model(**validated_data)
        if password is not None and not instance.is_superuser:
            instance.set_password(password)
            instance.save()
        return instance
