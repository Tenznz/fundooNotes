import logging

from rest_framework.views import APIView
from .utils import EncodeDecodeToken
from user.models import User
from user.serializers import UserSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import permissions

logging.basicConfig(filename="views.log", filemode="w")


class UserList(ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        try:
            return serializer.save(username=self.request.data.get('username'))
        except Exception as e:
            logging.error(e)

    def get_queryset(self):
        return self.queryset.filter(id=self.request.data.get("id"))


class UserLogin(APIView):
    """ class based views for user login """

    def post(self, request):
        """
        this method is use for user login
        :param request: username and password
        :return:response
        """
        try:
            user = auth.authenticate(username=request.data.get("username"), password=request.data.get("password"))
            if user is not None:
                UserSerializer(user)
                token = EncodeDecodeToken.encode_token(payload=user.pk)
                return Response(
                    {
                        "message": "login successfully", "data": token
                    },
                    status=status.HTTP_201_CREATED)

        except Exception as e:
            logging.error(e)
            return Response(
                {
                    "message": "user login unsuccessful"
                },
                status=status.HTTP_400_BAD_REQUEST)


# class ValidateToken(ListCreateAPIView):
#     serializer_class = UserSerializer
#     queryset = User.objects.all()
#     permission = (permissions.IsAuthenticated,)
#     lookup_field = "token"
#
#     def get_queryset(self):
#         print(self.request.data.get('token'))
#         # logging.info(EncodeDecodeToken().decode_token(token=self.request.data.get('token')))
#         return self.queryset.filter(id=self.request.data.get("id"))
