from django.urls import path
from .views import *

urlpatterns = [
    path("register",CreateAdminProfileAPIView.as_view(),name="register"),
    path("login",LoginAdminView.as_view(),name="login"),
    path("logout",LogoutView.as_view(),name="logout")
    ]
