from django.urls import path

from .views import *

urlpatterns = [
    path('get_token/<str:code>', get_access_token, name='get_access_token'),
    path('topics', get_topics),
    path('languages', get_languages),
    path('save_preferences/<int:user_id>', save_user_preferences),
    path('get_user_preferences/<int:user_id>', get_user_preferences)
]