from django.shortcuts import render
from .models import *
from rest_framework.views import APIView, Response
from django.http import HttpResponse
from django.core import serializers

class ArticleViewSet(APIView):

    @classmethod
    def get_extra_actions(cls):
        return []

    def get(self, *args, **kwargs):
        article = Article.objects.all()
        article_json = serializers.serialize('json', article)
        return HttpResponse(article_json)
