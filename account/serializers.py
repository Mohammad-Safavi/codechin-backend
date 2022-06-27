from django.contrib.auth import authenticate

from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from product.serializers import ProductSerializer, OptionSerializer
from .models import *


class CartSerializer(serializers.Serializer):
    product = ProductSerializer(read_only=True)
    options = OptionSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = '__all__'

    def create(self, validated_data):
        cart = Cart.objects.create(     
            product=validated_data['product'],
            options=validated_data['options'],
        )
        return cart