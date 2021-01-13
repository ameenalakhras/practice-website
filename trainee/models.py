from django.conf import settings
from django.db import models


class Trainee(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="trainee")
