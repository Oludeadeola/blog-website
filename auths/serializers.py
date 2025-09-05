from django.contrib.auth.password_validation import validate_password
from rest_framework.serializers import ModelSerializer

from auths.models import Blogger, Superuser
from auths.validators import EmailValidator


class CreateBloggerSerializer(ModelSerializer):

    class Meta:
        model = Blogger
        fields = [
            "first_name",
            "last_name",
            "email",
            "password",
            "username",
            "profile_image_url",
            "bio"
        ]
        read_only_fields = ["id", "uuid", "created_at", "last_updated"]
        extra_kwargs = {
            "password": {
                "write_only": True,
                "max_length": 128,
                "required": True,
                "allow_blank": False,
                "trim_whitespace": True,
                "allow_null": False,
                "validators": [validate_password],
            },
            "first_name": {
                "max_length": 120,
                "required": True,
                "allow_null": False,
                "allow_blank": False,
                "trim_whitespace": True,
            },
            "last_name": {
                "max_length": 120,
                "required": True,
                "allow_null": False,
                "allow_blank": False,
                "trim_whitespace": True,
            },
            "email": {
                "max_length": 120,
                "required": True,
                "allow_null": False,
                "allow_blank": False,
                "trim_whitespace": True,
                "validators": [EmailValidator()],
            },
            "username": {
                "max_length": 120,
                "required": True,
                "allow_null": False,
                "allow_blank": False,
                "trim_whitespace": True,
            },
            "profile_image_url": {
                "max_length": 500,
                "required": False,
                "allow_null": True,
                "allow_blank": True,
                "trim_whitespace": True,
            },
            "bio": {
                "max_length": 500,
                "required": False,
                "allow_null": True,
                "allow_blank": True,
                "trim_whitespace": True,
            },
        }


class CreateSuperuserSerializer(ModelSerializer):

    class Meta:
        model = Superuser
        fields = [
            "first_name",
            "last_name",
            "email",
            "password",
            "username",
            "profile_image_url",
        ]
        read_only_fields = ["id", "uuid", "created_at", "last_updated"]
        extra_kwargs = {
            "password": {
                "write_only": True,
                "max_length": 128,
                "required": True,
                "allow_blank": False,
                "trim_whitespace": True,
                "allow_null": False,
                "validators": [validate_password],
            },
            "first_name": {
                "max_length": 120,
                "required": True,
                "allow_null": False,
                "allow_blank": False,
                "trim_whitespace": True,
            },
            "last_name": {
                "max_length": 120,
                "required": True,
                "allow_null": False,
                "allow_blank": False,
                "trim_whitespace": True,
            },
            "email": {
                "max_length": 120,
                "required": True,
                "allow_null": False,
                "allow_blank": False,
                "trim_whitespace": True,
                "validators": [EmailValidator()],
            },
            "username": {
                "max_length": 120,
                "required": True,
                "allow_null": False,
                "allow_blank": False,
                "trim_whitespace": True,
            },
            "profile_image_url": {
                "max_length": 500,
                "required": False,
                "allow_null": True,
                "allow_blank": True,
                "trim_whitespace": True,
            },
        }
