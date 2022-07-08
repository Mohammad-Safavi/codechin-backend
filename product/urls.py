from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token  # <-- Here
from rest_framework import routers
from rest_framework.routers import DefaultRouter
from .views import *

router = routers.DefaultRouter()
router.register('list', ProductViewSet, basename='product')
router.register('comment', CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
    path('comment-list/<int:pk>/', CommentProductView.as_view()),
]
