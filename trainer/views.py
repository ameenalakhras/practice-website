from django.db.models import Q
from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from trainer.models import Trainer, TrainingRequest
from trainer.serializers import TrainerSerializer, TrainingRequestSerializer, TrainingRequestEditSerializer
from trainer.utils import send_training_push_notification_update


class TrainerViewSet(ListAPIView, CreateAPIView):
    queryset = Trainer.objects.all().order_by('id')
    serializer_class = TrainerSerializer
    permission_classes = (IsAuthenticated, )


class TrainingRequestViewSet(ListAPIView, CreateAPIView):
    queryset = TrainingRequest.objects.all().order_by('id')
    serializer_class = TrainingRequestSerializer
    permission_classes = (IsAuthenticated, )

    # create isn't required in the project requirements so i'll keep it available without much restrictions here.

    def get(self, request, *args, **kwargs):
        user = request.user
        self.queryset = self.get_queryset().filter(Q(trainer__user=user) | Q(trainee__user=user))
        return super(TrainingRequestViewSet, self).get(request, *args, **kwargs)


class TrainingRequestObjectViewSet(UpdateAPIView):
    queryset = TrainingRequest.objects.all().order_by('id')
    serializer_class = TrainingRequestEditSerializer
    permission_classes = (IsAuthenticated, )

    def patch(self, request, *args, **kwargs):
        user = request.user
        if user == self.get_object().trainer.user:
            response = super(TrainingRequestObjectViewSet, self).patch(self, request, *args, **kwargs)
            if response.status_code == 200:
                send_training_push_notification_update(updated_status=self.get_object().accepted)
            return response
        else:
            return Response(data={"message": "you're not authorized to do this request."},
                            status=status.HTTP_401_UNAUTHORIZED)

    def put(self, request, *args, **kwargs):
        return self.patch(request, *args, **kwargs)


