from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from rides.filters import RideFilter
from rides.models import Ride
from .models import Driver
from django.core.paginator import Paginator


# from django.contrib.auth.decorators import


def is_driver(user):
    return user.is_driver


# Create your views here.
@login_required
@user_passes_test(is_driver)
def ride_list(request: HttpRequest):
    context = {}
    # print(request.user)
    driver = Driver.objects.get(user=request.user)
    vehicle_type = driver.vehicle_type
    max_capacity = driver.max_capacity
    special_info = driver.special_info
    # print(special_info)
    filtered_rides = RideFilter(request.GET, queryset=Ride.objects.filter(status=Ride.RideStatus.OPEN,
                                                                          vehicle_type__in=["", vehicle_type],
                                                                          current_passengers_num__lte=max_capacity,
                                                                          special_request__in=["",
                                                                                               special_info]).order_by(
        'created_at'))

    context['filtered_rides'] = filtered_rides
    entry_number_per_page = 1
    paginated_filtered_rides = Paginator(filtered_rides.qs, entry_number_per_page)
    page_number = request.GET.get('page')
    rides_page_obj = paginated_filtered_rides.get_page(page_number)
    context['rides_page_obj'] = rides_page_obj
    return render(request, 'ride_list.html', context)
