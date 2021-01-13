from django.urls import path
from trainer.views import TrainerViewSet, TrainingRequestViewSet, TrainingRequestObjectViewSet

urlpatterns = [
    path("trainers", TrainerViewSet.as_view(), name="trainers"),
    path("training_requests", TrainingRequestViewSet.as_view(), name="training_requests"),
    path("training_requests/<int:pk>", TrainingRequestObjectViewSet.as_view(), name="training_request")
]
