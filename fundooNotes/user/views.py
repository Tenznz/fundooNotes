import logging

from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import auth
from rest_framework.response import Response
from user.models import User
from user.serializers import UserSerializer
from rest_framework.views import APIView
from .utils import EncodeDecodeToken
from rest_framework import status
from user.tasks import send_email_task

logging.basicConfig(filename="views.log", filemode="w")


class UserRegistration(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()

            token = EncodeDecodeToken.encode_token(payload=serializer.data['id'])
            send_email_task.delay(email=serializer.data["email"], token=str(token))
            return Response({
                "message": "data store successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            logging.error(e)
            return Response({
                'message': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logging.error(e)
            print(e)
            return Response(
                {
                    "message": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):

    def post(self, request):
        try:
            username = request.data.get("username")
            password = request.data.get("password")
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                UserSerializer(user)
                token = EncodeDecodeToken.encode_token(payload=user.pk)

                return Response({
                    "message": "login successfully",
                    "data": token
                }, status=status.HTTP_200_OK)
            return Response({
                "message": "user login unsuccessful"
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logging.error(e)
            return Response({
                "message": "login unsuccessful"
            }, status=status.HTTP_400_BAD_REQUEST)


class ValidateToken(APIView):
    def get(self, request, token):
        try:
            decoded_token = EncodeDecodeToken.decode_token(token=token)
            user = User.objects.get(id=decoded_token.get('id'))
            user.is_verified = True
            serializer = UserSerializer(user)
            return Response({
                "message": "Validation Successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logging.error(e)
            return Response({
                "message": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
