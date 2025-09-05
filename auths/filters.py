from django_filters import (
    FilterSet, NumberFilter, CharFilter,
)
from blog.models import Blogger

class BloggerFilter(FilterSet):

    email = CharFilter(field_name="email")
    username = CharFilter(field_name="username")

    class Meta:
        model = Blogger
        fields = ["email", "username"]
