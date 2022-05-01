import json
import logging

from django.contrib.auth.models import auth
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from user.models import User
from user.serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.decorators import api_view

logging.basicConfig(filename="views.log", filemode="w")


class UserRegistration(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.create(request.data)

            return Response({
                "message": "user login successfully",
                "data": serializer.data
            }, 201)
        except ValidationError:
            return Response({
                'message': serializer.errors
            }, 400)

        except Exception as e:
            logging.error(e)
            return Response({
                'message': str(e)
            }, 400)

    def get(self, request):
        try:
            users = User.objects.get(username=request.data.get("username"))
            serializer = UserSerializer(users)
            return Response({
                "message": "user found",
                "data": serializer.data
            })
        except ObjectDoesNotExist:
            return Response({
                "message": "user not found"
            }, 200)

        except Exception as e:
            return Response({
                "error_message": str(e)
            }, 400)  


class UserLogin(APIView):

    def post(self, request):
        try:
            user = auth.authenticate(username=request.data.get("username"), password=request.data.get("password"))
            if user is not None:
                serializer = UserSerializer(user)
                return Response({"message": "login successfully", "data": serializer.data}, 200)
            return Response({"message": "user login unsuccessful"}, 404)
        except Exception as e:
            logging.error(e)
            return Response({
                "message": str(e)
            }, 400)
