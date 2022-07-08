from xml.etree.ElementPath import xpath_tokenizer_re
from django.contrib.auth import authenticate

from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from product.serializers import ProductSerializer, OptionSerializer
from .models import *


class CartSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    options = OptionSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = '__all__'

class AddressSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Address
        fields = ('title', 'address', 'post_code')
    
    def create(self, validated_data):
        Address.objects.create(user=self.context['request'].user,**validated_data)
        return validated_data

class PaymentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Payment
        fields = ''
    
    def create(self, validated_data):
        cart_data = Cart.objects.filter(user=self.context['request'].user)
        payment = Payment.objects.create(user=self.context['request'].user,price=0,status=2)

        for x in cart_data:
            # invoice = Invoice()
            # invoice.payment=payment
            # invoice.product=x.product
            # invoice.count=x.count
            # invoice.save()
            # for x_ in x.options:
            #     invoice.options.add(x_)
            db = Invoice(product = x.product, count= x.count, payment=payment)
            db.save()
            db.options.add(x.options)

        return payment

class CreateCartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cart
        fields = ('product', 'options')
    
    def create(self, validated_data):
        if Cart.objects.filter(user=self.context['request'].user,product=validated_data['product']).exists() :
            raise serializers.ValidationError(
                {"error" : "این محصول در سبد خرید شما وجود دارد."})
        cart_data = Cart()
        cart_data.user=self.context['request'].user
        cart_data.product=validated_data['product']
        cart_data.save()
        cart_data.options.set(validated_data['options'])
        return cart_data

