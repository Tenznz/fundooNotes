from django.urls import path
from user import views

urlpatterns = [
    path('login', views.UserLogin.as_view()),
    path('register', views.UserRegistration.as_view()),
    # path('users', views.user_list)
]
