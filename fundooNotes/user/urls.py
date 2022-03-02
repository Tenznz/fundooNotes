from django.urls import path
from user import views


urlpatterns = [
    path('', views.homes, name="home"),
    path('login', views.UserLogin.as_view(), name="login"),
    path('register', views.UserRegistration.as_view(), name="register"),
]
