from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager



class User(AbstractUser):
    email = models.EmailField(unique=True)
    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = ["first_name", "last_name", "username"]

    objects = CustomUserManager()

    def __str__(self) -> str:
        return self.username

    @classmethod
    def get_regular_users(cls):
        return cls.objects.filter(is_staff=False)
