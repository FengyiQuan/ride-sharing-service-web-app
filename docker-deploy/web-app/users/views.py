from django.contrib.auth.forms import UserChangeForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpRequest
from django.contrib.auth import logout
from django.urls import reverse_lazy
from django.views import generic
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from django.contrib.auth.decorators import login_required
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

    # status  = 'undefined'
    # curUserInfo = User.objects.get(user = curUser)
    # username = curUserInfo.username
    # lastname = curUserInfo.lastname
    # firstname = curUserInfo.firstname
    # email = curUserInfo.email
    # # get vehicle info
    # driver = Driver.objects.get(user=curUser)
    # vehicle_type = driver.vehicle_type
    # max_capacity = driver.max_capacity
    # plate_num = driver.plate_num
    # special_info = driver.special_info
    data = User.objects.get(id=curUser.id)
    context = {
        'user_data': data,
    }
    return render(request, 'profile.html', context)


# @require_http_methods(["GET", "POST"])
@login_required
def editUserInfo(request: HttpRequest):
    if request.user.is_driver:
        form = userEditProfileForm(request.POST)
    if not form.is_valid():
        messages.error(request, form.errors)
        has_error = True
    # form = form.qq
    form = form.cleaned_data
    # username = form.get('username')
    email = form.get('email')
    lastname = form.get('lastname')
    firstname = form.get('firstname')
    User.objects.filter(id=request.user.id).update(
        email=email,
        # lastname=lastname,
        # firstname=firstname,
    )
    messages.success(request, f'Hi {request.user.get_short_name()}, your information have been changed.')
    return redirect('/profile')


class UserEditView(generic.UpdateView):
    # model = User
    # form_class = UserChangeForm
    template_name = 'editProfile.html'
    success_url = reverse_lazy('home')
    fields = ['username']

    def get_object(self):
        #     pass
        #     userId =
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
    fields = ['plate_num']
    template_name = 'driver_edit_profile.html'
    # slug_field = 'plate_num'
    # slug_url_kwarg = 'plate_num'

    success_url = reverse_lazy('home')

    #
    def get_object(self):
        # user_id =  request.user.id
        driver = Driver.objects.get(user=self.request.user)
