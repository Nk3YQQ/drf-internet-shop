from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {"blank": True, "null": True}


class Gender(models.TextChoices):
    """ Выбор гендера пользователя """

    MALE = 'male', 'Мужской'
    FEMALE = 'female', 'Женский'

class User(AbstractUser):
    """ Модель для пользователя """

    username = None
    first_name = models.CharField(max_length=150, verbose_name='Имя')
    last_name = models.CharField(max_length=150, verbose_name='Фамилия')
    birthday_date = models.DateField(verbose_name='Дата рождения', **NULLABLE)
    gender = models.CharField(max_length=6, choices=Gender.choices, verbose_name='Гендер')
    email = models.EmailField(unique=True, verbose_name='Электронная почта')
    avatar = models.ImageField(upload_to="users/profile/", verbose_name='Аватар', **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
