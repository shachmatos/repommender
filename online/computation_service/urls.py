from django.urls import path
from .views import *

urlpatterns = [
    path('fetch_channels/', fetch_recommendation_channels, name='fetch_recommendation_channels'),
]