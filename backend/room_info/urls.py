"""room_info urls"""
from django.urls import path
from . import views
urlpatterns = [
    path('list_room_calendar', views.list_room_calendar),
    path('list_colleges', views.list_colleges),
    path('get_curr_max_week', views.get_curr_max_week),
    path('look_answer_deque', views.look_answer_deque),
]
