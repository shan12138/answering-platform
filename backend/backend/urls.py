"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),
    path('teachers/', include('teachers.urls')),
    path('teachers/', include('room_info.urls')),
    path('teachers/', include('room_operation.urls')),
    path('students/', include('students.urls')),
    path('students/', include('room_info.urls')),
    path('students/', include('room_operation.urls')),
    path('admin_manage/', include('platform_system_admin.urls')),
    url(r'docs/', include_docs_urls(title="answering_platform")),
]
