from django.contrib.auth import get_user_model
from rest_framework import generics

from user.serializers import UserSerializer


class UserCreateView(generics.CreateAPIView):
    model = get_user_model()
    serializer_class = UserSerializer
