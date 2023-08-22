from rest_framework import serializers
from .models import *

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "password")

class AdminProfileCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'mobile','email',
                  'confirm_password']
