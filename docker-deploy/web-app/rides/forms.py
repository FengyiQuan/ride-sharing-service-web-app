from django import forms
from .models import SharedRequest


class RequestRideForm(forms.Form):
    destination = forms.CharField(label='destination', max_length=512)
    arrive_time = forms.DateTimeField(label='arrive_time')
    required_passengers_num = forms.IntegerField(label='required_passengers_num')
    vehicle_type = forms.CharField(label='vehicle_type', required=False)
    can_be_shared = forms.BooleanField(label='can_be_shared', required=False)
    special_request = forms.CharField(label='special_request', required=False)


class RideFilterForm(forms.Form):
    destination = forms.CharField(label='destination', max_length=512)
    vehicle_type = forms.CharField(label='vehicle_type', required=False)

    special_request = forms.CharField(label='special_request', required=False)
    # arrive_time = forms.(label='arrive_time')


class RideShareRequestForm(forms.Form):
    ride_id = forms.IntegerField(label='ride_id')
    earliest_arrive_date = forms.DateTimeField(label='earliest_arrive_date')
    latest_arrive_date = forms.DateTimeField(label='latest_arrive_date')
    required_passengers_num = forms.IntegerField(label='required_passengers_num')
    # class Meta:
    #     model = SharedRequest
    #     fields = ['ride_id', 'earliest_arrive_date', 'latest_arrive_date', 'required_passengers_num']
