from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model


User = get_user_model()


class CustomUser(AbstractUser):
    def __str__(self):
        return f'{self.first_name} {self.last_name}'
