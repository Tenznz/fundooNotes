from django.urls import path
from user import views


# schema_view = get_schema_view(
#    openapi.Info(
#       title="Snippets API",
#       default_version='v1',
#       description="Test description",
#       terms_of_service="https://www.google.com/policies/terms/",
#       contact=openapi.Contact(email="contact@snippets.local"),
#       license=openapi.License(name="BSD License"),
#    ),
#    public=True,
#    permission_classes=[permissions.AllowAny],
# )

urlpatterns = [
    path('login', views.UserLogin.as_view(), name="login"),
    path('register', views.UserRegistration.as_view(), name="registration"),
    path('validate/<str:token>', views.ValidateToken.as_view(), name='validate')
    # path('users', views.user_list)
]
