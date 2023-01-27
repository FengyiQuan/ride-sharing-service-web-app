from django.db import models
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

    def __str__(self):
        # destination = SharedRequest.objects.get(pk=id)
        return str(self.user)
