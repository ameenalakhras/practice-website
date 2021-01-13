from django.contrib.auth.models import AbstractUser
from django.db import models

import uuid


class User(AbstractUser):
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["username"]


    @staticmethod
    def generate_random_token():
        """generate a random string id then convert it to string"""
        random_id = uuid.uuid4()
        return str(random_id)

    def save(self, *args, **kwargs):
        create_request = self.id is None
        if create_request:
            self.registration_token = self.generate_random_token()
        return super(User, self).save(*args, **kwargs)
