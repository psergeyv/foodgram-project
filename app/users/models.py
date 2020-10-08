from django.db import models
from django.contrib.auth.models import AbstractUser

class Profile(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLE_CHOICES = [
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin'),
    ]
    role = models.CharField(
        max_length=30,
        choices=ROLE_CHOICES,
        default=USER,
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        default='',
        verbose_name="Номер телефона"
    )
    vk = models.CharField(
        max_length=100,
        blank=True,
        default='',
        verbose_name="Адрес страницы VK"
    )
    confirmation_code = models.CharField(
        max_length=30,
        blank=True,
        default=''
    )
    