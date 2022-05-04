import json
import logging
import jwt

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import ValidationError
from django.http import HttpResponse
from django.contrib.auth.models import auth
from rest_framework.response import Response
from user.models import User
from user.serializers import UserSerializer
from rest_framework.views import APIView
from .utils import EncodeDecodeToken, dictfetchall
from rest_framework import status
from user.task import send_email_task
from user.email import Email
from django.db import connection
from datetime import datetime

cursor = connection.cursor()

logging.basicConfig(filename="views.log", filemode="w")


class UserRegistration(APIView):
    """ class based views for User registration """

    @swagger_auto_schema(
        operation_summary="registration",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='username'),
                'first_name': openapi.Schema(type=openapi.TYPE_STRING, description='first_name'),
                'last_name': openapi.Schema(type=openapi.TYPE_STRING, description='last_name'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='password'),
                'age': openapi.Schema(type=openapi.TYPE_INTEGER, description='age'),
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='email'),
                'phone': openapi.Schema(type=openapi.TYPE_STRING, description='phone'),
            }
        ))
    def post(self, request):
        """
        this method is use for user Registration
        :param request: user_details
        :return:response
        """
        try:
            cursor.execute('INSERT into user_user (username,first_name,last_name,password,age,email,phone,'
                           'is_superuser,is_staff,is_active,date_joined,is_verified) values ( '
                           '%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                           [request.data.get('username'), request.data.get('first_name'),
                            request.data.get('last_name'), request.data.get('password'), request.data.get('age'),
                            request.data.get('email'), request.data.get('phone'), False, False, True,
                            datetime.now(), False
                            ])
            cursor.execute("select username,first_name,last_name,password,age,email,phone from user_user where "
                           "username=%s", [request.data.get("username")])
            return Response(
                {
                    "message": "data store successfully",
                    "data": dictfetchall(cursor)
                },
                status=status.HTTP_201_CREATED)

        except Exception as e:
            logging.error(e)
            print(e)
            return Response(
                {
                    "message": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="display",
    )
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

    @swagger_auto_schema(
        operation_summary="login",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='username'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='password'),
            }
        ))
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
                        "message": "login successfully", "data": token
                    },
                    status=status.HTTP_200_OK)
            return Response({
                'message': 'login unsuccessful'
            })

        except Exception as e:
            logging.error(e)
            return Response(
                {
                    "message": "user login unsuccessful"
                },
                status=status.HTTP_400_BAD_REQUEST)


class ValidateToken(APIView):
    """class based views for token validation"""

    @swagger_auto_schema(
        operation_summary="get user"
    )
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
