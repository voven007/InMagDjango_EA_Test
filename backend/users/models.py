from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from users.constants import MAX_LEN_EMAIL, MAX_LEN_USERNAME


class User(AbstractUser):
    """Модель прользователей"""
    email = models.EmailField(
        verbose_name='Электронная почта',
        max_length=MAX_LEN_EMAIL,
        unique=True
    )
    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=MAX_LEN_USERNAME,
        unique=True,
        validators=[RegexValidator(
            regex=r'^[\w.@+-]+$',
            message='Недопустимый символ в имени пользователя'
        )])
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=MAX_LEN_USERNAME
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=MAX_LEN_USERNAME
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'password']

    class Meta:
        ordering = ('username',)
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username
