from django.contrib.auth import authenticate

from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.response import Response


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
        ]


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, min_length=11)
    password = serializers.CharField(min_length=4, max_length=12)
    password_confirm = serializers.CharField(min_length=4, max_length=12)
    first_name = serializers.CharField(max_length=40)
    last_name = serializers.CharField(max_length=40)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        return user

    def validate_username(self, value):
        data = User.objects.filter(username=value).first()
        if data:
            raise serializers.ValidationError("حسابی با این شماره تماس وجود دارد.")
        return value
    
    def validate_password_confirm(self, value):
        data = self.initial_data
        if data['password'] != value:
            raise serializers.ValidationError("تکرار کلمه عبور اشتباه است.")
        return value
