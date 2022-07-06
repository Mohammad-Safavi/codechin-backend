from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token  # <-- Here
from .views import *


router = routers.DefaultRouter()
router.register('cart', CartViewSet, basename='cart')

urlpatterns = [
    path('', include(router.urls)),
    path('request/', send_request, name='request'),
    path('verify/', verify, name='verify'),
    path('cart/count/', CountCartView.as_view()),
]
