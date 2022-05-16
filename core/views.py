from rest_framework import permissions
from rest_framework import views, generics
from rest_framework.response import Response
from django.contrib.auth import *
from rest_framework import status

from . import serializers

class ProfileView(generics.RetrieveAPIView):
    serializer_class = serializers.UserSerializer

    def get_object(self):
        return self.request.user