import json
import logging

from django.contrib.auth.models import auth
from rest_framework.response import Response
from user.models import User
from user.serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError

logging.basicConfig(filename="views.log", filemode="w")


class UserRegistration(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({
                "message": "user store successfully",
                "data": serializer.data
            }, 201)
        except ValidationError:
            return Response({
                "message": serializer.error,
            }, 400)

        except Exception as e:
            logging.error(e)
            return Response({
                "message": str(e),
            }, 400)


class UserLogin(APIView):

    def post(self, request):
        try:
            user = auth.authenticate(username=request.data.get("username"), password=request.data.get("password"))
            if user is not None:
                serializer = UserSerializer(user)
                
                return Response({
                    "message": "login successfully",
                    "data": serializer.data}, 200)
            return Response({
                "message": "login unsuccessful"
            }, 400)
        except Exception as e:
            logging.error(e)
            return Response({
                "message": str(e)
            }, 400)
