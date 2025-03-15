from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('volunteer', 'Волонтер'),
        ('vulnerable', 'Вразлива людина'),
    )

    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='volunteer',
                                help_text='Тип користувача: волонтер або вразлива людина')
    phone = models.CharField(max_length=20, blank=True, null=True,
                           help_text='Контактний телефон користувача')
    bio = models.TextField(blank=True, null=True,
                         help_text='Коротка біографія або опис користувача')
    address = models.CharField(max_length=255, blank=True, null=True,
                             help_text='Адреса користувача')
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True,
                                    help_text='Зображення профілю користувача')

    def __str__(self):
        return self.username