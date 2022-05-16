from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token  # <-- Here
from .views import *

urlpatterns = [
    path('login/', obtain_auth_token,
         name='login'),  # <-- And here
    path('profile/', ProfileView.as_view()),
]
