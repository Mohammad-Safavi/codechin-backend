from django.contrib.auth import authenticate

from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
import random
from core.models import RegisterCode


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
    code = serializers.CharField(required=True)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        RegisterCode.objects.filter(username=validated_data['username'], code=validated_data['code']).delete()
        return user
            
    def validate_code(self, value):
        data = self.initial_data
        if RegisterCode.objects.filter(username=data['username'], code=value).exists():
            return value
        else :
            raise serializers.ValidationError(
                "کد وارد شده معتبر نمی باشد.")

    def validate_username(self, value):
        data = User.objects.filter(username=value).first()
        if data:
            raise serializers.ValidationError(
                "حسابی با این شماره تماس وجود دارد.")
        return value

    def validate_password_confirm(self, value):
        data = self.initial_data
        if data['password'] != value:
            raise serializers.ValidationError("تکرار کلمه عبور اشتباه است.")
        return value


class RegisterCodeSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    code = serializers.CharField(required=False)

    class Meta:
        model = RegisterCode
        fields = [
            'username',
            'code',
        ]

    def create(self, validated_data):
        username = validated_data['username']
        code = str(random.randrange(10000, 99999))
        if RegisterCode.objects.filter(code=code):
            code = str(random.randrange(10000, 99999))
        if RegisterCode.objects.filter(username=username).exists():
           RegisterCode.objects.filter(username=username).delete()
        res = RegisterCode.objects.create(username=username, code=code)
        return res

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                "حسابی با این شماره تماس وجود دارد.")
        return value
