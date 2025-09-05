from django_filters import (
    FilterSet, NumberFilter, CharFilter,
    DateTimeFilter, DateTimeFromToRangeFilter
)
from blog.models import Post

class PostFilter(FilterSet):

    blogger = NumberFilter(field_name="blogger")
    date = DateTimeFilter(field_name="created_at")
    date_from_to = DateTimeFromToRangeFilter()
    comment = NumberFilter()

    class Meta:
        model = Post
        fields = ["blogger", "date", "date_from_to", "comment"]
