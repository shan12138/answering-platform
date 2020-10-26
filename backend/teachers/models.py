"""teachers models"""
from django.db import models
from django.contrib.auth.models import User


class Teacher(models.Model):
    """the class of the teachers"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    real_name = models.CharField(max_length=15, null=True)
    email = models.EmailField(primary_key=True)
