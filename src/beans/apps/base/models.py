from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
