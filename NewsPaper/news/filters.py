from django.forms import DateTimeInput
from django_filters import FilterSet, DateTimeFilter
from .models import Post


class PostFilter(FilterSet):
    added_post = DateTimeFilter(
        field_name='date_time',
        lookup_expr='gt',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'},
        ),
    )


    class Meta:
        model = Post

        fields = {
            'heading': ['icontains'],
            'post_category': ['exact'],
            #'date_time': ['date__gt'],
        }
