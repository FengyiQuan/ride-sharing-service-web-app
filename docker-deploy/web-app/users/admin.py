from django.contrib import admin

# Register your models here.
# from .models import Order
from .models import Driver, User

admin.site.register(User)
# admin.site.register(Order)
admin.site.register(Driver)
