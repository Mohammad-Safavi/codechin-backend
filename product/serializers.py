from django.contrib.auth import authenticate

from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import *


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Picture
        fields = '__all__'

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = '__all__'

class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    pictures = PictureSerializer(many=True, read_only=True)
    properties = PropertySerializer(many=True, read_only=True)
    options = OptionSerializer(many=True, read_only=True)
    category = CategorySerializer(many=True, read_only=True)
    discount = DiscountSerializer(read_only=True)
    price = serializers.IntegerField(read_only=True)
    total = serializers.SerializerMethodField()

        
    class Meta:
        model = Product
        fields = '__all__'

    def get_total(self, obj):
        data = Product.objects.filter(id=obj.id)
        for x in data:
            sum = x.price
            if x.discount :
                sum =  x.price -(((x.price) * (x.discount.percent)/100))
        return int(sum)

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('product', 'text','status')
    
    def create(self, validated_data):
        comment = Comment()
        comment.product =validated_data['product']
        comment.text =validated_data['text']
        comment.status=2
        comment.user=self.context['request'].user
        comment.save()
        return validated_data

   