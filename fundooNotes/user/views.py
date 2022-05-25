import logging

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import auth
from rest_framework.response import Response
from user.models import User
from user.serializers import UserSerializer
from rest_framework.views import APIView
from .utils import EncodeDecodeToken
from rest_framework import status
from .producer import RabbitServer

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
        serializer = UserSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()

            token = EncodeDecodeToken.encode_token(payload=serializer.data['id'])
            RabbitServer().sign_up_message('user_signup', token, serializer.data)

            return Response(
                {
                    "message": "data store successfully",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED)

        except ValidationError as e:
            logging.error(e)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logging.error(e)
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
        total = User.objects.all().count()
        user = User.objects.all()[(total - 10):total]
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
                token = EncodeDecodeToken.encode_token(payload=user.pk)
                return Response(
                    {
                        "message": "login successfully",
                        "token": token
                    },
                    status=status.HTTP_201_CREATED)
            return Response(
                {
                    "message": "user not found"
                }, status=status.HTTP_201_CREATED)
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
            user = User.objects.get(id=decoded_token.get('id'))
            user.is_verified = True
            serializer = UserSerializer(user)
            return Response({"message": "Validation Successfully", "data": serializer.data},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            logging.error(e)
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
