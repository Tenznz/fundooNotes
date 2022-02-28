from django.urls import path
from user import views

urlpatterns = [
    path('login', views.UserLogin.as_view(), name="login"),
    path('validate/<str:token>', views.ValidateToken.as_view(), name='validate'),
    path('user', views.UserList.as_view(), name='user')
]
