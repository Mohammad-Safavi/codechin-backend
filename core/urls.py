from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token  # <-- Here
from .views import *


# router = routers.DefaultRouter()
# router.register('register', RegisterViewSet, basename='register')

urlpatterns = [
    # path('', include(router.urls)),
    path('login/', obtain_auth_token,
         name='login'),  # <-- And here
    path('register/', RegisterViewSet.as_view({'post' : 'post'})),
    path('register-code/', RegisterCodeView.as_view()),
    path('register-code-verify/', RegisterCodeVerifyView.as_view()),
    path('profile/', ProfileView.as_view()),
]
