from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from rest_framework import viewsets, status
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated


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
            return queryset.order_by('-created_at').all()
        else:
            return queryset.order_by('-created_at').all()[:int(num)]


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    def get_queryset(self):
        queryset = Comment.objects.filter(user=self.request.user)
        return queryset

    def destroy(self, request, *args, **kwargs):
        instance = Comment.objects.get(pk=kwargs['pk'],user=self.request.user)
        if not instance:
            return Response({'error':'شما مجوز حذف این دیدگاه را ندارید.'}, status=status.HTTP_204_NO_CONTENT)
        instance.delete()
        return Response({'success':'حذف با موفقیت انجام شد.'})

    def create(self, request, *args, **kwargs):
        serializer = CommentSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            if serializer.save():
                return Response({'success':'دیدگاه شما با موفقیت ثبت شد.'})


class CommentProductView(APIView):

    def get(self,request, *args, **kwargs):
        queryset = Comment.objects.filter(product=kwargs['pk'],status=1)
        return Response(CommentSerializer(queryset, many=True).data)
    