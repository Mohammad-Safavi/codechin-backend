from rest_framework import permissions
from rest_framework import views, generics
from rest_framework.viewsets import GenericViewSet
from rest_framework import viewsets
from rest_framework.mixins import CreateModelMixin
from rest_framework.views import APIView, Response
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
                return Response({'success':'ثبت نام کاربر با موفقیت انجام شد.'})

class RegisterCodeView(generics.CreateAPIView):
    serializer_class = serializers.RegisterCodeSerializer

class RegisterCodeVerifyView(APIView):
    def get(self, request, *args, **kwargs):
        username = request.query_params.get('username', None)
        code = request.query_params.get('code', None)
        if RegisterCode.objects.filter(username=username, code=code).exists():
            return Response({'success':'کد معتبر است.'})
        else:
            return Response({'error':'کد وارد شده نامعتبر است.'}, status=500)
 