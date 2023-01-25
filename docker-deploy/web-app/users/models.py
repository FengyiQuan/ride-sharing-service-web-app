from django.db import models
import django.utils.timezone
# Create your models here.

# from django.contrib.auth.models import User
from datetime import datetime

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_driver = models.BooleanField(default=False)


class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    vehicle_type = models.CharField(max_length=128)
    plate_num = models.CharField(max_length=128)
    max_capacity = models.PositiveIntegerField()
    special_info = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
