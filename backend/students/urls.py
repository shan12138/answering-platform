"""students urls"""
from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token
from . import views


urlpatterns = [
    path('', obtain_jwt_token),
    path('signup', views.signup),
    path('change_password', views.change_password),
    path('change_name', views.change_name),
    path('change_email', views.change_email),
    path('get_name', views.get_real_name),
    path('get_email', views.get_email),
    path('get_student_id', views.get_id),
    path('apply_ask', views.apply_to_ask),
    path('send_code', views.send_code),
    path('change_tele', views.change_tele)
]
