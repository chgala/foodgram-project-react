from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE


class User(AbstractUser):
    email = models.EmailField(
        verbose_name='Почта',
        unique=True
    )
    username = models.CharField(
        verbose_name='username',
        max_length=30,
        unique=True,
        null=True
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=30,
        null=True
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=40,
        null=True
    )

    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    USERNAME_FIELD = 'email'

    class Meta:
        # ordering = ('username', )
        verbose_name = 'User'
        verbose_name_plural = 'Users'
