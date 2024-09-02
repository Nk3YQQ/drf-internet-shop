from rest_framework import serializers

from users.models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    """ Модель сериализатора для регистрации пользователя"""

    password = serializers.CharField(write_only=True)
    passwordConfirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "email", "password", "password_confirm")

    def validate(self, attrs):
        password = attrs.get("password")
        password_confirm = attrs.get("passwordConfirm")

        if password != password_confirm:
            raise serializers.ValidationError("Пароли не совпадают")

        return attrs


class UserSerializer(serializers.ModelSerializer):
    """ Модель сериализатора для пользователя """

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'birthday_date', 'gender', 'email')
