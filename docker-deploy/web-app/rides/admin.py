from django.contrib import admin

# Register your models here.
from .models import Ride, SharedRequest

admin.site.register(Ride)
admin.site.register(SharedRequest)
