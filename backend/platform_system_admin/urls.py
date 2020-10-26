"""admin_manage urls"""
from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token
from . import views

urlpatterns = [
    path('', obtain_jwt_token),
    path('input_teacher', views.create_teacher),
    path('input_college', views.create_college),
]
