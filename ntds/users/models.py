from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    avatarimage = models.CharField(max_length=64, default='user-6380868_640.png')
    avatarlink = models.URLField(default='https://pub-72e635b4a3a44df194ab50509c42921e.r2.dev/user-6380868_640.png')

    def is_avatar_default(self):
        return self.avatarlink == 'https://pub-72e635b4a3a44df194ab50509c42921e.r2.dev/user-6380868_640.png'

    def __str__(self):
        return self.username