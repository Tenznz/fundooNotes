import json
import logging
import jwt
from django.contrib.auth.models import auth
from rest_framework.response import Response
from user.models import User
from user.serializers import UserSerializer
from rest_framework.views import APIView
from django.core.mail import send_mail
from .utils import EncodeDecodeToken
from rest_framework import status

logging.basicConfig(filename="views.log", filemode="w")


class UserRegistration(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            token = EncodeDecodeToken.encode_token(payload=serializer.data['id'])
            url = "http://127.0.0.1:8000/user/validate/" + str(token)
            send_mail("register", url, serializer.data['email'], ["dhugkar95@gmail.com"], fail_silently=False)
            return Response({
                "message": "data store successfully",
                "data": serializer.data
            }, 200)
        except Exception as e:
            logging.error(e)
            return Response({
                'message': str(e)
            }, 400)

    def get(self, request):
        user = User.objects.all()
        serializer = UserSerializer(user, many=True)
        return Response({"message": "data store successfully",
                         "data": serializer.data}, 200)


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
                    "token": token
                }, 200)
            return Response({
                "message": "user login unsuccessful"
            }, 400)
        except Exception as e:
            logging.error(e)
            return Response({
                'message': str(e)
            }, 400)


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
                'message': str(e)
            }, 400)
