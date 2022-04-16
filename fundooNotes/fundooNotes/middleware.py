# import logging
# import json
# from user.models import LoginData, User
# from rest_framework.reverse import reverse
#
# logging.basicConfig(filename="views.log", filemode="w")
#
#
# class CustomMiddleware:
#     """ middleware for login data """
#
#     def __init__(self, get_response):
#         self.get_response = get_response
#
#     def __call__(self, request):
#         """
#         adding to login_data table when user login
#         :param request:
#         :return:response
#         """
#         try:
#             if reverse("login"):
#                 # if self.get_response is not None:
#                 print("Welcome to FundooNotes Application")
#                 request_dict = json.loads(request.body)
#                 user = User.objects.get(username=request_dict.get("username"))
#                 response = self.get_response(request)
#                 login_data = LoginData(user_id_id=user.pk, token=response.data['data'])
#                 # print(f"total number of user : {user}")
#                 login_data.save()
#                 return response
#         except Exception as e:
#             logging.error(e)
#             return self.get_response(request)

