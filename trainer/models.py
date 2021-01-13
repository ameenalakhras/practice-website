from django.conf import settings
from django.db import models
from trainee.models import Trainee
from django.db.models.signals import post_save

from trainer.utils import send_training_request_push_notification


class Trainer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="media_publisher")
    trainees = models.ManyToManyField(Trainee, related_name="trainer_objects")


class TrainingRequest(models.Model):
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE, related_name="trainer_requests")
    trainee = models.ForeignKey(Trainee, on_delete=models.CASCADE, related_name="trainee_requests")
    accepted = models.BooleanField(null=True)
    sent_at = models.DateTimeField(auto_now_add=True)


post_save.connect(receiver=send_training_request_push_notification, sender=TrainingRequest)
