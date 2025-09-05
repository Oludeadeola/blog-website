from rest_framework import serializers


class TokenCreateSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)


class TokenSerializer(serializers.Serializer):
    access = serializers.CharField(required=False)
    refresh = serializers.CharField(required=False)


class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField(required=True)
