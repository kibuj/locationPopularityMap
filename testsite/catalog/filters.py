from django_filters import rest_framework as filters
from .models import Location

class LocationFilter(filters.FilterSet):
    rating_min = filters.NumberFilter(field_name="avg_rating", lookup_expr='gte')
    rating_max = filters.NumberFilter(field_name="avg_rating", lookup_expr='lte')

    class Meta:
        model = Location
        fields = [
            'category',
        ]