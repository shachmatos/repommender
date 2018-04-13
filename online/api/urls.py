from django.urls import path
from .views import *

urlpatterns = [
    path('test_token/<str:code>', get_access_token, name='get_access_token'),
]