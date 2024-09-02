from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from users.models import User
from users.permissions import IsAdmin
from users.serializers import UserRegistrationSerializer, UserSerializer


@extend_schema_view(create=extend_schema(description="Register a new user"))
class UserRegistrationAPIView(generics.CreateAPIView):
    """Создание пользователя"""

    serializer_class = UserRegistrationSerializer
    permission_classes = [IsAdmin]


@extend_schema_view(retrieve=extend_schema(description="Read a current user"))
class CurrentUserAPIView(generics.RetrieveAPIView):
    """Чтение текущего пользователя"""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
