from django.shortcuts import render
from django.http import HttpRequest

from django.views.decorators.http import require_http_methods, require_GET, require_POST


# Create your views here.

@require_GET
def home(request: HttpRequest):
    return render(request, 'home.html')
