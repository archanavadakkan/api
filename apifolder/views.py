from django.contrib.auth import login, logout
from rest_framework import generics

from .serializers import *
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password, check_password


class CreateAdminProfileAPIView(APIView):
    """
       View for admin Registration
    """
    permission_classes = []  # disables permission
    serializer_class = AdminProfileCreateSerializer

    def post(self, request):
        data = request.data
        serializer = AdminProfileCreateSerializer(data=data)
        if serializer.is_valid():
            password = request.data['password']
            confirm_password = request.data['confirm_password']
            if password == confirm_password:
                password1 = make_password(data['password'])  # encrypt the password
                password2 = make_password(data['confirm_password'])  # encrypt the password
                serializer.save(admin=True, password=password1, confirm_password=password2)
                email = serializer.data['email']
                id = serializer.data['id']
                data = User.objects.get(email=email)
                result = {
                    "id": id,
                    "email": data.email,
                }

                return Response(result, status=200)
            else:
                return Response("wrong_password")
        else:
            return Response(serializer.errors, status=400)


class LoginAdminView(APIView):
    """
        View for admin login
    """
    permission_classes = []
    serializer_class = AdminSerializer

    def post(self, request):
        email = request.data['username']
        password = request.data['password']
        try:
            user = User.objects.get(username=email)
            user_id = user.id
            user_email = user.email
            if user and check_password(password, user.password):
                login(request, user)
                token, created = Token.objects.get_or_create(user=user.id)
                result = {
                    'id': user_id,
                    'username': user_email,
                    'token': token.key
                }
                return Response(result, status=200)
            return Response("Invalid password")
        except User.DoesNotExist:
            return Response('Error')


class LogoutView(APIView):
    """
    Logout
    """

    def get(self, request):
        # request.user.auth_token.delete()
        logout(request)
        return Response('logged out')
