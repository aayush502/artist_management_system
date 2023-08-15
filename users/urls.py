from django.urls import path
from .views import *

urlpatterns = [
    path('user-list/', user_list, name='user-list'),
    path('user-update/<int:pk>', user_update, name='user-update'),
]