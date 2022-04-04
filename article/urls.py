from django.urls import path, include
from .views import *

urlpatterns = [
    path('', ArticleViewSet.as_view()),
]