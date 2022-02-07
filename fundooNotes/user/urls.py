from django.urls import path

from user import views

urlpatterns = [
    path('login', views.login),
    path('register', views.user_register),
    path('users', views.users)
]
