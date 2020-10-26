"""admin models"""
from django.db import models


# Create your models here.
class College(models.Model):
    """the class of the college"""
    name = models.CharField(unique=True, max_length=20, null=True)
