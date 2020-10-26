"""teachers urls"""
from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token
from . import views


urlpatterns = [
    path('', obtain_jwt_token),
    path('change_password', views.change_password),
    path('change_name', views.change_name),
    path('get_name', views.get_teacher_name),
    path('get_email', views.get_teacher_email),
    path('change_queue', views.change_queue),
    path('confirm_teachers', views.confirm_teachers),
    path('ban_students', views.ban_students),
    path('close_ban_students', views.close_ban_students),
    path('open_living', views.open_living),
    path('close_living', views.close_living),
    path('delete_room_calendar', views.delete_room_calendar),
    path('list_room_students', views.list_room_students),
    path('own_rooms', views.list_own_rooms),
    path('resolved_rooms', views.list_resolved_rooms),
    path('create_room', views.create_room),
    path('create_room_calendar', views.create_room_calendar),
    path('alter_room', views.alter_room),
    path('alter_room_calendar', views.alter_room_calendar),
    path('confirm_students', views.confirm_students),
    path('get_all_calendars', views.get_all_calendars),
    path('cancel_confirm_students', views.cancel_confirm_students),
]
