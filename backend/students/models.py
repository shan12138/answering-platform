"""students models"""
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Student(models.Model):
    """the class of students"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    real_name = models.CharField(max_length=15, null=True)
    telephone = models.CharField(max_length=11, unique=True, blank=True, null=True)


class VerifyCode(models.Model):
    """the class of verifyCode"""
    mobile = models.CharField(max_length=11)
    code = models.CharField(max_length=6)
    add_time = models.DateTimeField(default=datetime.now())
