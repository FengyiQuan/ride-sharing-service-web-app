from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .forms import RequestRideForm, RideShareRequestForm
from django.contrib import messages
from .models import Ride, SharedRequest
from .filters import RideFilter
from django.forms.models import model_to_dict
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError

# Create your views here.
entry_number_per_page = 5


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
        # print(form_data.get('can_be_shared'))
        if has_error:
            # return JsonResponse({"a":"asd"})
            return render(request, 'request_ride.html', {'form': form_data})
        else:
            user = request.user
            new_ride_request = Ride(owner=user, destination=destination, arrive_time=arrive_time,
                                    current_passengers_num=required_passengers_num,
                                    vehicle_type=vehicle_type, can_be_shared=can_be_shared,
                                    special_request=special_request)
            try:
                new_ride_request.full_clean()
                new_ride_request.save()
                messages.success(request,
                                 f'Hi {user.get_short_name()}, your request to {new_ride_request.destination} was created. ')
                return redirect('/')
            except ValidationError as e:
                non_field_errors = e.message_dict[NON_FIELD_ERRORS]
                messages.error(request, non_field_errors)
                return render(request, 'request_ride.html', {'form': form_data})
    else:
        return render(request, 'request_ride.html')


@require_GET
@login_required
def show_all_ride_list(request: HttpRequest):
    context = {}
    filtered_rides = RideFilter(request.GET, queryset=Ride.objects.all())
    context['filtered_rides'] = filtered_rides

    paginated_filtered_rides = Paginator(filtered_rides.qs, entry_number_per_page)
    page_number = request.GET.get('page')
    rides_page_obj = paginated_filtered_rides.get_page(page_number)
    context['rides_page_obj'] = rides_page_obj
    return render(request, 'ride_list.html', context)


@require_GET
@login_required
def user_ride_list(request: HttpRequest):
    context = {}
    user = request.user
    shared_ride = SharedRequest.objects.filter(sharer=user)
    queryset = Ride.objects.filter(can_be_shared=True, status=Ride.RideStatus.OPEN).exclude(
        owner=user, id__in=[r.id for r in shared_ride]).order_by('arrive_time')
    filtered_rides = RideFilter(request.GET, queryset=queryset)
    context['filtered_rides'] = filtered_rides
    paginated_filtered_rides = Paginator(filtered_rides.qs, entry_number_per_page)
    page_number = request.GET.get('page')
    rides_page_obj = paginated_filtered_rides.get_page(page_number)
    context['rides_page_obj'] = rides_page_obj
    return render(request, 'ride_list.html', context)


@require_POST
@login_required
def create_shared_request(request: HttpRequest):
    form = RideShareRequestForm(request.POST)

    if form.is_valid():
        form_data = form.cleaned_data
        sharer = request.user
        ride_id = form_data.get('ride_id')
        ride = Ride.objects.get(id=ride_id, can_be_shared=True, status=Ride.RideStatus.OPEN)
        if not ride:
            return JsonResponse({'error': 'no such ride or ride cannot be shareds'})
        earliest_arrive_date = form_data.get('earliest_arrive_date')
        latest_arrive_date = form_data.get('latest_arrive_date')
        required_passengers_num = form_data.get('required_passengers_num')

        new_shared_request = SharedRequest(sharer=sharer, ride=ride, earliest_arrive_date=earliest_arrive_date,
                                           latest_arrive_date=latest_arrive_date,
                                           required_passengers_num=required_passengers_num)
        try:
            new_shared_request.full_clean()
            new_shared_request.save()
            ride.current_passengers_num += required_passengers_num
            ride.save()
            messages.success(request, 'share request create successful')
            return JsonResponse({'shared_request': model_to_dict(new_shared_request)}, safe=False)
        except ValidationError as e:
            non_field_errors = e.message_dict[NON_FIELD_ERRORS]
            messages.error(request, non_field_errors)
            return JsonResponse({'error': non_field_errors}, status=400)
    else:
        messages.error(request, form.errors)
        return JsonResponse({'error': form.errors}, status=400)


@login_required
@require_POST
def complete_ride(request: HttpRequest, ride_id: int):
    user = request.user
    ride = Ride.objects.get(id=ride_id, owner=user)
    if not ride:
        messages.error(request, "ride does not exist or it does not belong to you. ")
        return JsonResponse({'error': "unable to complete a non-confirmed ride"}, status=400)
    elif ride.status != Ride.RideStatus.CONFIRMED:
        messages.error(request, "unable to complete a non-confirmed ride")
        return JsonResponse({'error': "unable to complete a non-confirmed ride"}, status=400)
    else:
        pass
