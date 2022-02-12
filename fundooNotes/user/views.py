import json
import logging

from django.contrib.auth.models import auth
from django.http import JsonResponse
from rest_framework.response import Response
from user.models import User
from user.serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser

logging.basicConfig(filename="views.log", filemode="w")


class UserRegistration(APIView):
    def post(self, request):
        data = JSONParser().parse(request)
        serializer = UserSerializer(data=data)
        try:
            if serializer.is_valid(raise_exception=True):
                user = User.objects.create_user(username=serializer.data['username'],
                                                first_name=serializer.data['first_name'],
                                                last_name=serializer.data['last_name'],
                                                password=serializer.data['password'],
                                                age=serializer.data['age'],
                                                email=serializer.data['email'],
                                                phone=serializer.data['phone'])

                user.save()
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
                serializer = UserSerializer(user)
                return Response({"message": "login successfully", "data": serializer.data["username"]})
                # return Response({"message": "user login successful", "data": username})
            else:
                return JsonResponse({"message": "user login unsuccessful"})
        except Exception as e:
            logging.error(e)
            return JsonResponse({"message": "login unsuccessful"})
