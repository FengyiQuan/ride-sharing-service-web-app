from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from rides.filters import RideFilter
from rides.models import Ride
from .models import Driver
from users.models import User
from django.core.paginator import Paginator
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from django.contrib import messages
from django.forms.models import model_to_dict
from django.core.mail import send_mail
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError

# from django.contrib.auth.decorators import
entry_number_per_page = 5


def is_driver(user):
    return user.is_driver


# Create your views here.
@login_required
@user_passes_test(is_driver)
@require_GET
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
    paginated_filtered_rides = Paginator(filtered_rides.qs, entry_number_per_page)
    page_number = request.GET.get('page')
    rides_page_obj = paginated_filtered_rides.get_page(page_number)
    context['rides_page_obj'] = rides_page_obj
    context['driver_view'] = True
    return render(request, 'ride_list.html', context)


@login_required
@user_passes_test(is_driver)
@require_GET
def confirmed_ride_list(request: HttpRequest):
    context = {}
    driver = Driver.objects.get(user=request.user)
    filtered_rides = RideFilter(request.GET, queryset=Ride.objects.filter(status=Ride.RideStatus.CONFIRMED,
                                                                          driver=driver).order_by(
        '-arrive_time'))

    context['filtered_rides'] = filtered_rides
    paginated_filtered_rides = Paginator(filtered_rides.qs, entry_number_per_page)
    page_number = request.GET.get('page')
    rides_page_obj = paginated_filtered_rides.get_page(page_number)
    context['rides_page_obj'] = rides_page_obj
    context['driver_view'] = True
    return render(request, 'ride_list.html', context)


@login_required
@user_passes_test(is_driver)
@require_POST
def confirm_ride(request: HttpRequest, ride_id: int):
    ride = Ride.objects.get(id=ride_id)

    if ride.status != Ride.RideStatus.OPEN:
        messages.error(request, 'cannot confirm ride that is not open.')
        return JsonResponse({'error': 'cannot confirm ride that is not open.'}, status=400)
    driver = Driver.objects.get(user=request.user)
    # print(driver)
    ride.driver = driver
    ride.status = Ride.RideStatus.CONFIRMED
    try:
        ride.full_clean()
        ride.save()
        send_mail(
            'Here is the message',
            'As a ride-owner, your ride has been comfirmed',
            'no-reply@ride-app.com',
            [ride.owner.email],
            fail_silently=False,
        )
        sharer = User.objects.filter(id == ride.sharer.all().values_list('id', flat=True))
        if sharer:
            send_mail(
                'Here is the message',
                'As a ride-sharer, your ride has been confirmed',
                'no-reply@ride-app.com',
                [sharer.email],
                fail_silently=False,
            )
        messages.success(request, f'ride for user {ride.owner} confirmed successful. ')
        return JsonResponse({'ride': model_to_dict(ride)}, safe=False)
    except ValidationError as e:
        non_field_errors = e.message_dict[NON_FIELD_ERRORS]
        messages.error(request, non_field_errors)
        return JsonResponse({'error': non_field_errors}, status=400)


@login_required
@user_passes_test(is_driver)
@require_POST
def complete_ride(request: HttpRequest, ride_id: int):
    user = request.user
    ride = Ride.objects.get(id=ride_id, driver=user)
    if not ride:
        messages.error(request, "ride does not exist or it does not belong to you as a driver. ")
        return JsonResponse({'error': "ride does not exist or it does not belong to you as a driver. "}, status=400)
    elif ride.status != Ride.RideStatus.CONFIRMED:
        messages.error(request, "unable to complete a non-confirmed ride")
        return JsonResponse({'error': "unable to complete a non-confirmed ride"}, status=400)
    else:
        ride.status = Ride.RideStatus.COMPLETE
        try:
            ride.full_clean()
            ride.save()
            messages.success(request, f'ride for user {ride.owner} complete successful. ')
            return JsonResponse({'ride': model_to_dict(ride)}, safe=False)
        except ValidationError as e:
            non_field_errors = e.message_dict[NON_FIELD_ERRORS]
            messages.error(request, non_field_errors)
            return JsonResponse({'error': non_field_errors}, status=400)
