from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse

from django.views.decorators.http import require_http_methods, require_GET, require_POST
from django.contrib.auth.decorators import login_required
from .forms import RequestRideForm
from django.contrib import messages
from .models import Ride


# Create your views here.

@require_GET
def home(request: HttpRequest):
    return render(request, 'home.html')


@require_http_methods(["GET", "POST"])
@login_required
def request_ride(request: HttpRequest):
    if request.method == "POST":
        form = RequestRideForm(request.POST)
        has_error = False

        if not form.is_valid():
            messages.error(request, form.errors)
            has_error = True

        form_data = form.cleaned_data

        destination = form_data.get('destination')
        arrive_time = form_data.get('arrive_time')
        required_passengers_num = form_data.get('required_passengers_num')
        vehicle_type = form_data.get('vehicle_type')
        can_be_shared = form_data.get('can_be_shared')
        special_request = form_data.get('special_request')
        # print(can_be_shared)
        if has_error:
            # return JsonResponse({"a":"asd"})
            return render(request, 'request_ride.html', {'form': form_data})
        else:
            # count = User.objects.filter(username=username).count()
            # if count != 0:
            #     messages.error(request, 'User already exist. ')
            #     return render(request, 'register.html', {'form': form_data})
            # else:
            user = request.user
            ride_request = Ride.objects.create(owner=user, destination=destination, arrive_time=arrive_time,
                                               current_passengers_num=required_passengers_num,
                                               vehicle_type=vehicle_type, can_be_shared=can_be_shared,
                                               special_request=special_request)
            # user = User.objects.create_user(username, email, password)
            # print(user.get_short_name())
            messages.success(request,
                             f'Hi {user.get_short_name()}, your request to {ride_request.destination} was created. ')
            return redirect('/')
    else:
        return render(request, 'request_ride.html')


def ride_list(request: HttpRequest):
    rides = Ride.objects.all()
    return render(request, 'ride_list.html', {'ride_list': rides, })
