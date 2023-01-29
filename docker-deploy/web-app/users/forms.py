from django import forms


# class LoginForm(forms.Form):
#     username = forms.CharField(label='username', max_length=100)
#     password = forms.CharField(label='password', required=False)


class RegisterUserForm(forms.Form):
    username = forms.CharField(label='username', max_length=100)
    email = forms.CharField(label='email', max_length=100)
    password = forms.CharField(label='password')
    password2 = forms.CharField(label='password2')


class RegisterDriverForm(forms.Form):
    vehicle_type = forms.CharField(label='vehicle_type', max_length=128)
    plate_num = forms.CharField(label='plate_num', max_length=128)
    max_capacity = forms.IntegerField(label='max_capacity')
    special_info = forms.CharField(label='special_info', required=False)

class driverUserEditProfileForm(forms.Form):
    vehicle_type = forms.CharField(label='vehicle_type', max_length=128)
    plate_num = forms.CharField(label='plate_num', max_length=128)
    max_capacity = forms.IntegerField(label='max_capacity')


class userEditProfileForm(forms.Form):
    username = forms.CharField(label='username', max_length=100)
    email = forms.CharField(label='email', max_length=100)
    lastname = forms.CharField(label='lastname')
    firstname = forms.CharField(label='firstname')

