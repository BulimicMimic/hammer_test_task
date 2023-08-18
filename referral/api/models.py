from django.contrib.auth.models import AbstractUser
from django.core.validators import (
    RegexValidator,
    MinValueValidator,
    MaxValueValidator,
)
from django.db import models


class User(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        null=True,
        blank=True,
    )
    phone_regex = RegexValidator(
        regex=r'^\+7\d{10}$',
        message="Phone number must be entered in the format: '+79999999999'.",
        )
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=12,
        unique=True,
    )
    user_invite_code = models.CharField(
        max_length=6,
        unique=True,
        null=True,
        blank=True,
    )
    activated_code = models.CharField(
        max_length=6,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return str(self.phone_number)


class AuthorizationCode(models.Model):
    user = models.ForeignKey(
        User,
        related_name='authorization_code',
        on_delete=models.CASCADE,
    )
    authorization_code = models.IntegerField(
        null=True,
        blank=True,
        validators=(
            MinValueValidator(0),
            MaxValueValidator(9999)
        ),
        error_messages={
            'validators': 'Код авторизации должен быть от 0 до 9999'}
    )
