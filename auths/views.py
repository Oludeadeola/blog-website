from rest_framework.mixins import CreateModelMixin, UpdateModelMixin
from rest_framework.generics import GenericAPIView

from auths.models import Blogger, User, Superuser
from auths.permissions import AllowAny, IsAdminUser, IsAuthenticatedUser
from auths.serializers import CreateBloggerSerializer, CreateSuperuserSerializer
from auths.filters import BloggerFilter
from rest_framework import status
from rest_framework.response import Response

from auths.utils import send_registration_successful_mail


# Create your views here.
def create_user(self, serializer):
    serializer.is_valid(raise_exception=True)
    saved_user: User = self.perform_create(serializer)
    send_registration_successful_mail(
        to=[serializer.validated_data.get("email")],
        name=serializer.validated_data.get("first_name"),
        subject=self.EMAIL_SUBJECT,
        template=self.template_name
    )
    headers = self.get_success_headers(self.get_serializer(saved_user).data)
    return headers, saved_user


class BloggerAPIView(GenericAPIView):
    # queryset = ALL_BLOGGERS_QUERYSET
    serializer_class = CreateBloggerSerializer
    filter_class = BloggerFilter
    search_fields = ["username", "email", "id", "uuid", "created_at"]
    ordering_fields = ["username", "created_at"]
    ordering = ["-created_at"]
    permission_classes = [AllowAny]


class BloggerCreateUpdateView(CreateModelMixin, UpdateModelMixin, BloggerAPIView):
    template_name = "registration_successful.html"
    EMAIL_SUBJECT = "Registration Was Successful"

    def post(self, request, *args, **kwargs):
        serializer: CreateBloggerSerializer = self.get_serializer(data=request.data)
        headers, saved_user = create_user(self, serializer)
        return Response(self.get_serializer(saved_user).data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer: CreateBloggerSerializer) -> User:
        saved_user: User = Blogger.objects.create_user(**serializer.validated_data)
        return saved_user

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class SuperUserCreateUpdateView(GenericAPIView, CreateModelMixin, UpdateModelMixin):
    serializer_class = CreateSuperuserSerializer
    template_name = "registration_successful.html"
    EMAIL_SUBJECT = "Registration Was Successful"

    def post(self, request, *args, **kwargs):
        serializer: CreateSuperuserSerializer = self.get_serializer(data=request.data)
        headers, saved_user = create_user(self, serializer)
        return Response(self.get_serializer(saved_user).data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer: CreateSuperuserSerializer) -> User:
        saved_user: User = Superuser.objects.create_superuser(**serializer.validated_data)
        return saved_user

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def get_permissions(self):
        return [IsAdminUser, IsAuthenticatedUser]
