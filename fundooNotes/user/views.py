import json
import logging
from django.contrib.auth.models import auth, User
from django.http import JsonResponse

# from user.models import User

# Create your views here.


logging.basicConfig(filename="views.log", filemode="w")


def login(request):
    # if request.method == "POST":
    user_dict = json.loads(request.body)
    user_name = user_dict.get("username")
    try:
        if auth.authenticate(username=user_name, password=user_dict.get("password")):
            return JsonResponse({"message": "user login successfully", "data": {"username": user_name}})
        else:
            return JsonResponse({"message": "user login unsuccessful", "data": {"username": user_name}})
    except Exception as e:
        logging.error(e)
        # return Response({"message":"user registred successfully","data":{"username":username}})


def user_register(request):
    try:
        if request.method == "POST":
            user_dict = json.loads(request.body)
            username = user_dict.get('username')
            if not User.objects.filter(username=username).exists():
                user = User(username=username, first_name=user_dict.get('firstname'),
                            last_name=user_dict.get('lastname'), password=user_dict.get('password'),
                            email=user_dict.get('email'))
                logging.info(f"user: {user}")
                user.save()
                return JsonResponse({"message": "user registered successfully", "data": {"username": username}})
            else:
                return JsonResponse({"message": "user register unsuccessful"})
    except Exception as e:
        logging.error(e)


def users(request):
    data = list(User.objects.values())
    return JsonResponse(data, safe=False)
