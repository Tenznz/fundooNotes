import json
import logging

from django.http import HttpResponse, JsonResponse
from user.models import User

# Create your views here.


logging.basicConfig(filename="views.log", filemode="w")


def login(request):
    if request.method != "POST":
        return JsonResponse({
            "message": "works post request only"
        })
    user_dict = json.loads(request.body)
    user_name = user_dict.get("username")
    try:
        if User.objects.filter(username=user_name, password=user_dict.get("password")):
            return JsonResponse({"message": "user login successfully", "data": {"username": user_name}})
        else:
            return JsonResponse({"message": "user login unsuccessful", "data": {"username": user_name}})
    except Exception as e:
        logging.error(e)
        return JsonResponse({"message": str(e)})


def user_register(request):
    try:
        if request.method == "POST":
            user_dict = json.loads(request.body)
            username = user_dict.get('username')
            if not User.objects.filter(username=username):
                user = User(username=username, firstname=user_dict.get('first_name'),
                            lastname=user_dict.get('last_name'), password=user_dict.get('password'),
                            age=int(user_dict.get('age')),
                            email=user_dict.get('email'), phone=user_dict.get('phone'))
                logging.info(f"user: {user}")
                user.save()
                return JsonResponse({"message": "user registered successfully", "data": {"username": username}})
            else:
                return JsonResponse({"message": "user register unsuccessful"})
    except Exception as e:
        logging.error(e)
        return JsonResponse({
            'message': str(e)
        })


def users(request):
    data = list(User.objects.values())
    return JsonResponse({'data': data}, safe=False)
