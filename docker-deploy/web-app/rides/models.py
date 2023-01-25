from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from users.models import User, Driver
from django.utils.translation import gettext_lazy as _


class Ride(models.Model):
    class RideStatus(models.TextChoices):
        OPEN = 'OPEN', _('OPEN')
        CONFIRMED = 'CONFIRMED', _('CONFIRMED')
        CLOSED = 'CLOSED', _('CLOSED')

    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, default=None, on_delete=models.CASCADE, null=True)
    destination = models.TextField(max_length=512)
    arrive_time = models.DateTimeField()
    current_passengers_num = models.IntegerField(default=1)
    vehicle_type = models.TextField(max_length=128, null=True)
    other_request = models.TextField()
    status = models.CharField(default=RideStatus.OPEN, max_length=10,
                              choices=RideStatus.choices)  # OPEN, CANCELLED, CLOSE, CONFIRMED
    can_be_shared = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class SharedRequest(models.Model):
    id = models.AutoField(primary_key=True)
    sharer = models.ForeignKey(User, on_delete=models.CASCADE)
    ride_id = models.ForeignKey(Ride, on_delete=models.CASCADE, null=True)
    earliest_arrive_date = models.DateTimeField(help_text='Format: 2020-01-01 12:00')
    latest_arrive_date = models.DateTimeField(help_text='Format: 2020-01-01 13:00')
    required_passengers_num = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
