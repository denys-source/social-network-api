from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    last_active = models.DateTimeField(null=True)

    @property
    def name(self) -> str:
        return f"{self.first_name} {self.last_name}"
