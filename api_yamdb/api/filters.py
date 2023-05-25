from django_filters import rest_framework as django_filters
from reviews.models import Title

# Взято из документации по джанго по фильтрации
# https://ilyachch.gitbook.io/django-rest-framework-russian-documentation/
# overview/navigaciya-po-api/filtering

# https://django-filter.readthedocs.io/en/stable/ref/filterset.html
# И немного взято отсюда


class TitleFilter(django_filters.FilterSet):
    genre = django_filters.CharFilter(lookup_expr='slug')
    category = django_filters.CharFilter(lookup_expr='slug')

    class Meta:
        model = Title
        fields = '__all__'
