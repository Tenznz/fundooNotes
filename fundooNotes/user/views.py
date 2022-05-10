import json
import logging

from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import auth
from rest_framework.response import Response
from user.models import User
from user.serializers import UserSerializer
from rest_framework.views import APIView
from .utils import EncodeDecodeToken
from rest_framework import status
from user.task import send_email_task
from user.email import Email


logging.basicConfig(filename="views.log", filemode="w")


class UserRegistration(APIView):
    """ class based views for User registration """

    def post(self, request):
        """
        this method is use for user Registration
        :param request: user_details
        :return:response
        """
        serializer = UserSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                {
                    "message": "data store successfully",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED)
        except ValidationError:
            return Response({
                "message": serializer.error,
            }, 400)
        except Exception as e:
            logging.error(e)
            print(e)
            return Response(
                {
                    "message": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        """
        this method get user details
        :param request:
        :return:response
        """
        user = User.objects.raw("select * from user_user;")
        print(user)
        serializer = UserSerializer(user, many=True)
        return Response({
            "message": "data fetch successfully",
            "data": serializer.data
        },
            status=status.HTTP_200_OK)


class UserLogin(APIView):
    """ class based views for user login """

    def post(self, request):
        """
        this method is use for user login
        :param request: username and password
        :return:response
        """
        try:
            username = request.data.get("username")
            password = request.data.get("password")
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                UserSerializer(user)
                token = EncodeDecodeToken.encode_token(payload=user.pk)
                return Response(
                    {
                        "message": "login successfully", "token": token
                    },
                    status=status.HTTP_200_OK)
            return Response({
                'message': 'login unsuccessful'
            }, 400)

        except Exception as e:
            logging.error(e)
            return Response(
                {
                    "message": "user login unsuccessful"
                },
                status=status.HTTP_400_BAD_REQUEST)


class ValidateToken(APIView):
    """class based views for token validation"""

    def get(self, request, token):
        """
        this method is use for get token
        :param request:
        :param token:
        :return:response
        """
        try:
            decoded_token = EncodeDecodeToken.decode_token(token=token)
            print(type(decoded_token.get('id')), decoded_token.get('id'))
            id = decoded_token.get('id')
            user = User.objects.raw(f"SELECT * FROM user_user where id = {id};")
            print(user)
            user.is_verified = True
            serializer = UserSerializer(user, many=True)
            return Response({"message": "Validation Successfully", "data": serializer.data},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            logging.error(e)
            return HttpResponse(e, status=status.HTTP_400_BAD_REQUEST)
