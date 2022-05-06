from django.urls import path
from user import views

urlpatterns = [
    path('login', views.UserLogin.as_view(), name="login"),
    path('register', views.UserRegistration.as_view(), name="registration"),
    # path('users', views.user_list)
]
