from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token  # <-- Here
from rest_framework import routers
from rest_framework.routers import DefaultRouter
from .views import *

router = routers.DefaultRouter()
router.register('', ProductViewSet, basename='product')

urlpatterns = [
    path('', include(router.urls)),
]
