import json
import logging
from django.contrib.auth.models import auth
from django.http import JsonResponse

from user.models import UserProfile

# Create your views here.


logging.basicConfig(filename="views.log", filemode="w")


def login(request):
    if request.method == "POST":
        user_dict = json.loads(request.body)
        print(user_dict)
        username = user_dict.get("username")
        print(username)
        try:
            # if auth.authenticate(username=username, password=user_dict.get("password")):
            user = auth.authenticate(username=username, password=user_dict.get("password"))
            print(user)
            if user is not None:
                print("Reached inside if")
                return JsonResponse({"message": "user login successfully", "data": {"username": username}})
            else:
                return JsonResponse({"message": "user login unsuccessful", "data": {"username": username}})
        except Exception as e:
            logging.error(e)
            return JsonResponse({"message": "login unsuccessful"})


def user_register(request):
    try:
        if request.method == "POST":
            user_dict = json.loads(request.body)
            username = user_dict.get('username')
            if not UserProfile.objects.filter(username=username).exists():
                user = UserProfile(username=username, first_name=user_dict.get('first_name'),
                                   last_name=user_dict.get('last_name'),
                                   age=int(user_dict.get('age')),
                                   email=user_dict.get('email'), phone=user_dict.get('phone'))
                logging.info(f"user: {user}")
                user.set_password(user_dict.get('password'))
                user.save()
                return JsonResponse({"message": "user registered successfully", "data": {"username": username}})
            else:
                return JsonResponse({"message": "user register unsuccessful"})
    except Exception as e:
        logging.error(e)
        return JsonResponse({"message": "user register unsuccessful"})


def users(request):
    data = list(UserProfile.objects.values())
    return JsonResponse(data, safe=False)
