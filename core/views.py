from rest_framework import permissions
from rest_framework import views, generics
from rest_framework.viewsets import GenericViewSet
from rest_framework import viewsets
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from django.contrib.auth import *
from rest_framework import status
from .serializers import *

from . import serializers


class ProfileView(generics.RetrieveAPIView):
    serializer_class = serializers.UserSerializer

    def get_object(self):
        return self.request.user


class RegisterViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = serializers.RegisterSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            if serializer.save():
                return Response({'success':'register user successfully.'})