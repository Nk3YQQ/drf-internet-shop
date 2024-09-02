from django.urls import path

from users.apps import UsersConfig
from users.views import UserRegistrationAPIView, CurrentUserAPIView

app_name = UsersConfig.name

urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name='user_registration'),
    path('profile/', CurrentUserAPIView.as_view(), name='current_user')
]