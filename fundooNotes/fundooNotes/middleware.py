import logging
import json
from user.models import LoginData, User
from rest_framework.reverse import reverse

logging.basicConfig(filename="views.log", filemode="w")


class CustomMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def process_exception(self, request, exception):
        logging.exception(exception)

    def __call__(self, request):

        response = self.get_response(request)
        try:
            if request.path == '/user/login':
                request_dict = json.loads(request.body)
                user = User.objects.get(username=request_dict.get("username"))
                LoginData.objects.create(user_id_id=user.pk, token=response.data['token'])
        except Exception as e:
            raise e
        return response

    # @staticmethod
    # def login_check(request):

# def simple_middleware(get_response):
#     # One-time configuration and initialization.
#
#     def middleware(request):
#         # Code to be executed for each request before
#         # the view (and later middleware) are called.
#
#         response = get_response(request)
#
#         # Code to be executed for each request/response after
#         # the view is called.
#
#         return response
#
#     return middleware
