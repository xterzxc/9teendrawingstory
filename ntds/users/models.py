from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    def str(self):
        return self.username