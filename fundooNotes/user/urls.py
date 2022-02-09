from django.urls import path
# from rest_framework.urlpatterns import format_suffix_patterns
from user import views

urlpatterns = [
    path('login', views.UserLogin.as_view()),
    path('register', views.UserRegistration.as_view())
    # path('users', views.users)
]
