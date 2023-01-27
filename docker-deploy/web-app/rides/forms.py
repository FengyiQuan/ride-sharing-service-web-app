from django import forms


class RequestRideForm(forms.Form):
    destination = forms.CharField(label='destination', max_length=512)
    arrive_time = forms.DateTimeField(label='arrive_time')
    required_passengers_num = forms.IntegerField(label='required_passengers_num')
    vehicle_type = forms.CharField(label='vehicle_type', required=False)
    can_be_shared = forms.BooleanField(label='can_be_shared', required=False)
    special_request = forms.CharField(label='special_request', required=False)
