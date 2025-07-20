from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    pass  # no email field, defaults from AbstractUser

    def __str__(self):
        return self.username