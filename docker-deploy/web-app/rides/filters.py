import django_filters
from django.db import models
from .models import Ride
from .forms import RideFilterForm
from django.forms import DateTimeInput


class RideFilter(django_filters.FilterSet):
    # destination = django_filters.CharFilter(lookup_expr='icontains')
    arrive_times = django_filters.DateTimeFromToRangeFilter(field_name="arrive_time", label='Arrive time range',
                                                            lookup_expr=('icontains'),
                                                            widget=django_filters.widgets.RangeWidget(
                                                                attrs={'type': 'datetime-local'}
                                                            ))
    # arrive_times_end = django_filters.TimeRangeFilter(field_name="arrive_time", lookup_expr='gte')
    # vehicle_type = django_filters.CharFilter(lookup_expr='icontains')
    # special_request = django_filters.CharFilter(lookup_expr='icontains')
    seats_needed = django_filters.NumberFilter(label='seats needed', method='filter_by_seats')

    class Meta:
        model = Ride
        fields = {'destination': ['icontains'],
                  'vehicle_type': ['icontains'],
                  'special_request': ['icontains']}
        # form = RideFilterForm

    # filter_overrides = {
    #     models.CharField: {
    #         'filter_class': django_filters.CharFilter,
    #         'extra': lambda f: {
    #             'lookup_expr': 'icontains',
    #         },
    #     },
    #     models.BooleanField: {
    #         'filter_class': django_filters.BooleanFilter,
    #         'extra': lambda f: {
    #             'widget': forms.CheckboxInput,
    #         },
    #     },
    def filter_by_seats(self, queryset, name, value):
        return queryset
