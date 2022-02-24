import logging
from user.models import User

logging.basicConfig(level=logging.INFO, file='sample.log')


class CustomMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print("Welcome to FundooNotes Application")
        user = User.objects.all().count()
        print(f"total number of user : {user}")
        response = self.get_response(request)
        return response
