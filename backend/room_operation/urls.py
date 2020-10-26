"""room_operation urls"""
from django.urls import path
from . import views

urlpatterns = [
    path('search_room', views.search_room_by_condition),
    path('search_room_info', views.search_room_info),
    path('enter_password', views.enter_password),
    path('enter_room', views.enter_room),
]
