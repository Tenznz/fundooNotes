import json
import logging
import jwt

from django.shortcuts import render
from drf_yasg import openapi
from rest_framework.exceptions import ValidationError
from django.http import HttpResponse
from django.contrib.auth.models import auth
from rest_framework.response import Response
from user.models import User
from user.serializers import UserSerializer
from rest_framework.views import APIView
from .utils import EncodeDecodeToken
from rest_framework import status
from user.task import send_email_task
from user.email import Email
from django.views.decorators.csrf import csrf_exempt

logging.basicConfig(filename="views.log", filemode="w")


def homes(request):
    return render(request, 'register.html', {})


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
            user = User.objects.create_user(username=serializer.data['username'],
                                            first_name=serializer.data['first_name'],
                                            last_name=serializer.data['last_name'],
                                            password=serializer.data['password'],
                                            age=serializer.data['age'],
                                            email=serializer.data['email'],
                                            phone=serializer.data['phone'])

            token = EncodeDecodeToken.encode_token(payload=user.pk)
            print(token)
            return render(request, 'login.html')
        except ValidationError as e:
            logging.error(e)
            # return render(request, 'display.html', {'result': serializer.errors})
            return render(request, 'register.html')

        except Exception as e:
            logging.error(e)
            print(e)
        return HttpResponse(request, e)

    def get(self, request):
        """
        this method get user details
        :param request:
        :return:response
        """
        user = User.objects.all()
        serializer = UserSerializer(user, many=True)
        return render(request, 'display.html', {'result': serializer.data})


class UserLogin(APIView):
    """ class based views for user login """

    # @csrf_exempt
    def post(self, request):
        """
        this method is use for user login
        :param request: username and password
        :return:response
        """

        try:
            # print(request.POST['username'])
            # print(request.data.get('password'))
            username = request.data.get("username")
            password = request.data.get("password")
            user = auth.authenticate(username=username, password=password)
            print(user.pk)
            if user is not None:
                serializer = UserSerializer(user)
                token = EncodeDecodeToken.encode_token(payload=user.pk)
                print(token)
                return render(request, 'display.html', {'result': serializer.data})

        except Exception as e:
            logging.error(e)
            return HttpResponse(request, 'display.html', {'result': e})
