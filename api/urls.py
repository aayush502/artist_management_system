from django.urls import path
from .views import *

urlpatterns = [
    path('user-list/', userList, name='user-list'),
    path('user-update/<int:pk>', updateUser, name='user-update'),
    path('user-delete/<int:pk>', deleteUser, name='user-delete'),
]