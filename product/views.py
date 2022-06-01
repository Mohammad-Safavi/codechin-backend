from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from rest_framework import viewsets
from .models import *
from .serializers import *


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def get_queryset(self):
        queryset = Product.objects
        stdi = self.request.query_params.get('is_discount', None)
        num = self.request.query_params.get('page_size',None)
        if stdi == 'true':
            queryset = Product.objects.filter(~Q(discount=None))
        if num == None:
            return queryset.all()
        else:
            return queryset.all()[:int(num)]
