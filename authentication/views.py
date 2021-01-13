from authentication.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from authentication.serializer import UserSerializer, UserLoginSerializer, UserTraineeLoginSerializer
from trainee.models import Trainee
from trainer.models import Trainer


class RegisterUser(CreateAPIView):
    model = User
    permission_classes = ()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        registration_type = request.data.get("type", "trainee")
        if registration_type == "trainer" or registration_type == "trainee":

            response = super(RegisterUser, self).post(request, *args, **kwargs)
            if response.status_code == 201:
                user = User.objects.get(username=response.data.get("username"))
                if registration_type == "trainer":
                    Trainer.objects.create(user=user)
                else:
                    Trainee.objects.create(user=user)
                return response

        else:
            return Response(data={"message": "registration type must be trainer or trainee"},
                            status=status.HTTP_400_BAD_REQUEST)


class UserLoginAPIView(GenericAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        # i made the login with the default django token here for simplicity.
        email = request.data.get("email")
        user_exists = User.objects.filter(email=email).exists()
        if user_exists:
            user = User.objects.get(email=email)
            try:
                # check if the user is a trainer
                user.trainer
            except AttributeError:
                self.serializer_class = UserTraineeLoginSerializer

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.user
            token, _ = Token.objects.get_or_create(user=user)
            return Response(
                data={"token": token.key},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
