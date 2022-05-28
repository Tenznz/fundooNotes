import logging

from django.shortcuts import render
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import auth
from user.models import User
from user.serializers import UserSerializer
from rest_framework.views import APIView
from .utils import EncodeDecodeToken

logging.basicConfig(filename="views.log", filemode="w")


def homes(request):
    return render(request, 'Register.html', {})


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
            print(serializer.data)
            token = EncodeDecodeToken.encode_token(payload=serializer.data['id'])
            print(token)
            return render(request, 'login.html')
        except ValidationError as e:
            logging.error(e)
            # return render(request, 'display.html', {'result': serializer.errors})
            return render(request, 'register.html')

        except Exception as e:
            logging.error(e)
            print(e)
            return render(request, 'error.html', {'result': str(e)})

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
            print(user.pk)
            if user is not None:
                serializer = UserSerializer(user)
                token = EncodeDecodeToken.encode_token(payload=user.pk)
                print(token)
                return render(request, 'display.html', {'result': serializer.data})

        except Exception as e:
            logging.error(e)
            return render(request, 'error.html', {'result': str(e)})
