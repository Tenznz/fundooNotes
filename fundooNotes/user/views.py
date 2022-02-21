import json
import logging
import jwt
from django.http import HttpResponse
from django.contrib.auth.models import auth
from django.http import JsonResponse
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
            user = User.objects.create_user(username=serializer.data['username'],
                                            first_name=serializer.data['first_name'],
                                            last_name=serializer.data['last_name'],
                                            password=serializer.data['password'],
                                            age=serializer.data['age'],
                                            email=serializer.data['email'],
                                            phone=serializer.data['phone'])

            token = EncodeDecodeToken.encode_token(payload=user.pk)
            print(token)
            decoded_token = EncodeDecodeToken.decode_token(token=token)
            print(decoded_token)
            url = "http://127.0.0.1:8000/user/validate/" + str(token)
            print(url)
            # send_mail(subject, message, from_email, [to_email], fail_silently=False)
            send_mail("register", url, serializer.data['email'], ["dhugkar95@gmail.com"], fail_silently=False)
            return Response({"message": "data store successfully",
                             "data": {"username": serializer.data}})

        except Exception as e:
            logging.error(e)
            return JsonResponse(serializer.errors)

    def get(self, request):
        user = User.objects.all()
        serializer = UserSerializer(user, many=True)
        return JsonResponse(serializer.data, safe=False)


class UserLogin(APIView):

    def post(self, request):
        try:
            username = request.data.get("username")
            password = request.data.get("password")
            user = auth.authenticate(username=username, password=password)
            print(user)
            if user is not None:
                UserSerializer(user)
                token = EncodeDecodeToken.encode_token(payload=user.pk)

                return Response({"message": "login successfully", "data": token})
                # return Response({"message": "user login successful", "data": username})
            else:
                return JsonResponse({"message": "user login unsuccessful"})
        except Exception as e:
            logging.error(e)
            return JsonResponse({"message": "login unsuccessful"})


class ValidateToken(APIView):
    def get(self, request, token):
        try:
            print(token)
            decoded_token = EncodeDecodeToken.decode_token(token=token)
            print(decoded_token)
            user = User.objects.get(id=decoded_token.get('id'))
            user.is_verified = True
            serializer = UserSerializer(user)
            return Response({"message": "Validation Successfully", "data": serializer.data},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            logging.error(e)
            return HttpResponse(e)
