from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from users.models import User
from drivers.models import Driver
from django.utils.translation import gettext_lazy as _
import json
from django.core.exceptions import ValidationError


class Ride(models.Model):
    class RideStatus(models.TextChoices):
        OPEN = 'OPEN', _('OPEN')
        CONFIRMED = 'CONFIRMED', _('CONFIRMED')
        COMPLETE = 'COMPLETE', _('COMPLETE')
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

    def clean(self):
        share_requests = SharedRequest.objects.filter(sharer=self.owner)
        for request in share_requests:
            if self.arrive_time < request.earliest_arrive_date or self.arrive_time > request.latest_arrive_date:
                raise ValidationError("arrive_time not match other request's schedule")
        # TODO: driver info match validator
        if self.driver is None:
            return
        elif self.status == self.RideStatus.OPEN:
            raise ValidationError("open ride is not allowed to have a driver ")
        else:
            # driver = self.driver.foreign_related_fields
            driver_max_capacity = self.driver.max_capacity
            driver_special_info = self.driver.special_info
            driver_vehicle_type = self.driver.vehicle_type
            if driver_max_capacity > self.current_passengers_num and driver_special_info != self.special_request and (
                    self.vehicle_type or driver_vehicle_type != self.vehicle_type):
                raise ValidationError("your profile does not match request ride. ")
    # def to_json(self):
    #     return json.dumps(self, default=lambda o: o.__dict__)


class SharedRequest(models.Model):
    id = models.AutoField(primary_key=True)
    sharer = models.ForeignKey(User, on_delete=models.CASCADE)
    ride = models.ForeignKey(Ride, on_delete=models.CASCADE)
    earliest_arrive_date = models.DateTimeField(help_text='Format: 2020-01-01 12:00')
    latest_arrive_date = models.DateTimeField(help_text='Format: 2020-01-01 13:00')
    required_passengers_num = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        # destination = SharedRequest.objects.get(pk=id)
        return f"{self.required_passengers_num} shared {self.ride}"

    def clean(self):
        if self.earliest_arrive_date >= self.latest_arrive_date:
            raise ValidationError('from time should be before to time')
        # ride = Ride.objects.get(id=self.ride_id)
        if self.ride.arrive_time < self.earliest_arrive_date or self.ride.arrive_time > self.latest_arrive_date:
            raise ValidationError("time range not in owner's schedule")
    #
    # def to_json(self):
    #     return json.dumps(self, default=lambda o: o.__dict__)
