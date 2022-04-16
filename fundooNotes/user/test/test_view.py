import pytest

from rest_framework.reverse import reverse
from user.models import User
from user.serializers import UserSerializer
from django.contrib.auth import get_user_model

pytestmark = pytest.mark.django_db


class TestUser:
    # @pytest.mark.django_db
    # def setUp(self):
    #     self.user = User.objects.create_user(username='Ten', first_name="Ten", last_name="Duk", password='Duk',
    #                                          email='duk@gmail,com',
    #                                          phone='9191919191', is_verified='True', age=20)

    # @pytest.mark.django_db
    # def setUp(self):
    # self.client = Client()
    # self.user = get_user_model().objects.create_user(
    #     username='Ten', password='Duk', email='duk@gmail,com', phone='9191919191', is_verified='True', age=20)

    @pytest.mark.django_db
    def test_user(self, client):
        url = reverse("registration")
        user = {
            "username": "Tenzin2",
            "first_name": "Ten",
            "last_name": "duk",
            "password": "1234",
            "age": 26,
            "email": "duk@gmail.com",
            "phone": "1234567890",
            "is_verified": 0
        }
        print(url)
        response = client.post(url, user)
        print(response.content)
        assert response.status_code == 201

    @pytest.mark.django_db
    def testlogin(self, client):
        user = User.objects.create_user(username="Tenzin",
                                        first_name="Ten",
                                        last_name="duk",
                                        password="1234",
                                        age=26,
                                        email="duk@gmail.com",
                                        phone="1234567890",
                                        is_verified=0
                                        )
        user.save()
        data = {
            "username": "Tenzin",
            "password": "1234",
        }
        url = reverse("login")
        response = client.post(url, data)
        assert response.status_code == 201
    # @pytest.mark.django_db
    # def test_login(self, client):
    #     url = reverse('login')
    #     login_data = {'username': 'Ten', 'password': 'Duk'}
    #     respone = client.post(url, login_data,)
    #
    #     assert respone.status_code == 201


