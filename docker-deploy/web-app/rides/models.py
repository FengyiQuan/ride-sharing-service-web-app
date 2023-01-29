from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from users.models import User
from drivers.models import Driver
from django.utils.translation import gettext_lazy as _
import json


class Ride(models.Model):
    class RideStatus(models.TextChoices):
        OPEN = 'OPEN', _('OPEN')
        CONFIRMED = 'CONFIRMED', _('CONFIRMED')
        CLOSED = 'CLOSED', _('CLOSED')

    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, blank=True, on_delete=models.CASCADE, null=True)
    destination = models.CharField(max_length=512)
    arrive_time = models.DateTimeField()
    current_passengers_num = models.IntegerField(default=1)
    # available_capacity = models.IntegerField(default=1)
    vehicle_type = models.CharField(max_length=128, blank=True)
    special_request = models.TextField(blank=True)
    status = models.CharField(default=RideStatus.OPEN, max_length=10,
                              choices=RideStatus.choices)  # OPEN, CANCELLED, CLOSE, CONFIRMED
    can_be_shared = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.destination

    # def to_json(self):
    #     return json.dumps(self, default=lambda o: o.__dict__)


class SharedRequest(models.Model):
    id = models.AutoField(primary_key=True)
    sharer = models.ForeignKey(User, on_delete=models.CASCADE)
    ride_id = models.ForeignKey(Ride, on_delete=models.CASCADE, null=True)
    earliest_arrive_date = models.DateTimeField(help_text='Format: 2020-01-01 12:00')
    latest_arrive_date = models.DateTimeField(help_text='Format: 2020-01-01 13:00')
    required_passengers_num = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        # destination = SharedRequest.objects.get(pk=id)
        return f"{self.required_passengers_num} shared {self.ride_id}"
    #
    # def to_json(self):
    #     return json.dumps(self, default=lambda o: o.__dict__)
