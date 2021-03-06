from django.urls import path
from authentication.views import RegisterUser, UserLoginAPIView, LogoutView

urlpatterns = [
    path("register", RegisterUser.as_view(), name="register_user"),
    path("login", UserLoginAPIView.as_view(), name="login"),
    path("logout", LogoutView.as_view(), name="logout"),
]
