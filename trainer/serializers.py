from rest_framework import serializers
from trainer.models import Trainer, TrainingRequest


class TrainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trainer
        fields = "__all__"


class TrainingRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingRequest
        fields = "__all__"


class TrainingRequestEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingRequest
        fields = ("accepted", )
