from django.contrib.auth.forms import UserChangeForm
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpRequest
from django.contrib.auth import logout
from django.urls import reverse_lazy
from django.views import generic
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from django.contrib.auth.decorators import login_required

from rides.models import SharedRequest, Ride
from .models import User
from drivers.models import Driver
from .forms import RegisterUserForm, RegisterDriverForm, driverUserEditProfileForm, \
    userEditProfileForm


@require_POST
def logout_view(request):
    logout(request)


@require_http_methods(["GET", "POST"])
def register(request: HttpRequest):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        has_error = False

        if not form.is_valid():
            messages.error(request, form.errors)
            has_error = True

        form_data = form.cleaned_data
        username = form_data.get('username')
        email = form_data.get('email')
        password = form_data.get('password')
        password2 = form_data.get('password2')

        if password != password2:
            messages.error(request, 'Password does not match. ')
            has_error = True
        if has_error:
            return render(request, 'register.html', {'form': form_data})
        else:
            count = User.objects.filter(username=username).count()
            if count != 0:
                messages.error(request, 'User already exist. ')
                return render(request, 'register.html', {'form': form_data})
            else:
                user = User.objects.create_user(username, email, password)
                print(user.get_short_name())
                messages.success(request, f'Hi {user.get_short_name()}, your account was created. Please log in. ')
                return redirect('/user/login')
    else:
        return render(request, 'register.html')


@require_http_methods(["GET", "POST"])
@login_required
def register_driver(request: HttpRequest):
    if request.method == "POST":
        form = RegisterDriverForm(request.POST)
        has_error = False

        if not form.is_valid():
            messages.error(request, form.errors)
            has_error = True

        form_data = form.cleaned_data
        # print(form_data)
        vehicle_type = form_data.get('vehicle_type')
        plate_num = form_data.get('plate_num')
        max_capacity = form_data.get('max_capacity')
        special_info = form_data.get('special_info')

        if has_error:
            return render(request, 'register.html', {'form': form_data})
        else:
            current_user = request.user
            current_user.is_driver = True
            current_user.save()
            driver = Driver.objects.create(user=current_user, vehicle_type=vehicle_type, plate_num=plate_num,
                                           max_capacity=max_capacity, special_info=special_info)
            # if count != 0:
            #     messages.error(request, 'User already exist. ')
            #     return render(request, 'register.html', {'form': form_data})
            # else:
            #     user = User.objects.create_user(username, email, password)
            #     print(user.get_short_name())
            print('driver', driver)
            # messages.success(request, f'Hi {user.get_short_name()}, your account was created. Please log in. ')
            return redirect('/')
    else:
        return render(request, 'register_driver.html')


# R6
# Get /driverInfo
# @require_http_methods(["GET", "POST"])
@login_required
def viewUserInfo(request: HttpRequest):
    curUser = request.user
    # TODO what is driver status here?
    data = User.objects.get(id=curUser.id)
    context = {
        'user_data': data,
    }
    return render(request, 'profile.html', context)

class UserEditView(generic.UpdateView):
    template_name = 'editProfile.html'
    success_url = reverse_lazy('profile')
    fields = ['username', 'email','first_name','last_name']
    def get_object(self):
        return self.request.user


@require_http_methods(["GET", "POST"])
@login_required
def viewDriverInfo(request: HttpRequest):
    curUser = request.user
    driver_data = Driver.objects.get(user=curUser)
    context = {
        'driver_data': driver_data,
    }
    return render(request, 'driver_profile.html', context)


@require_http_methods(["GET", "POST"])
@login_required
def editDriverInfo(request: HttpRequest):
    if request.user.is_driver:
        form = driverUserEditProfileForm(request.POST)

        vehicle_type = form.get('vehicle_type')
        max_capacity = form.get('max_capacity')
        plate_num = form.get('plate_num')

        Driver.objects.filter(user=request.user).update(vehicle_type=vehicle_type,
                                                        max_capacity=max_capacity,
                                                        plate_num=plate_num)

        messages.success(request, f'Hi {request.user.get_short_name()}, your profile has been changed. ')
        return redirect('/driverprofile')


class driverEditView(generic.UpdateView):
    model = Driver
    fields = ['plate_num','max_capacity','vehicle_type']
    template_name = 'driver_edit_profile.html'
    success_url = reverse_lazy('driverprofile')
    def get_object(self):
        driver = Driver.objects.get(user=self.request.user)
        return driver

@require_GET
@login_required
def userRidesView(request: HttpRequest):
    context = {}
    user = request.user
    owmed_ride = Ride.objects.filter(owner=user).exclude(status=Ride.RideStatus.CLOSED)
    # TODO: fix the query here
    shared_ride = SharedRequest.objects.filter(sharer=user)

    paginated_owned_rides = Paginator(owmed_ride, 5)
    page_number = request.GET.get('page')
    owned_rides_page_obj = paginated_owned_rides.get_page(page_number)
    context['owned_rides_page_obj'] = owned_rides_page_obj

    paginated_shared_rides = Paginator(shared_ride, 5)
    page_number = request.GET.get('page')
    shared_rides_page_obj = paginated_shared_rides.get_page(page_number)
    context['shared_rides_page_obj'] = shared_rides_page_obj

    return render(request, 'user_rides.html', context)


@require_GET
@login_required
def userDetailsOwnedRidesView(request: HttpRequest, id):
    context = {}
    # user = request.user
    owned_ride = Ride.objects.get(id=id)
    context['ride_obj'] = owned_ride
    return render(request, 'owned_one_ride.html', context)
@require_GET
@login_required
def userDetailsSharedRidesView(request: HttpRequest, id):
    context = {}
    # user = request.user
    # todo: fix query
    owned_ride = SharedRequest.objects.get(id=id)
    context['ride_obj'] = owned_ride
    return render(request, 'owned_one_ride.html', context)

class ownedRideEditView(generic.UpdateView):
    model = Ride
    fields = ['destination']
    template_name = 'owned_ride_edit.html'
    success_url = reverse_lazy('user_rides')
    def get_object(self, *args, **kwargs):
        ride = Ride.objects.get(id=self.kwargs.get('id'))
        return ride

class sharedRideEditView(generic.UpdateView):
    model = Ride
    fields = ['sharer']
    template_name = 'shared_ride_edit.html'
    success_url = reverse_lazy('user_rides')
    def get_object(self, *args, **kwargs):
        sharedRequest = SharedRequest.objects.get(id=self.kwargs.get('id'))
        return sharedRequest
