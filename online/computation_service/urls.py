from django.urls import path
from .views import *

urlpatterns = [
    path('<int:user_id>/fetch_channels/', fetch_recommendation_channels, name='fetch_recommendation_channels'),
]