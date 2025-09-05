from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt import views as jwt_views
from rest_framework_simplejwt.settings import api_settings as jwt_settings
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from auths.models import User
from auths.permissions import AllowAny
from auths.token.serializers import (
    TokenCreateSerializer,
    RefreshTokenSerializer,
    TokenSerializer,
)
from auths.utils import TOKEN_CREATE_AUTHENTICATION_FAILED_FOR_USER, EMAIL, PASSWORD


class TokenCreateView(jwt_views.TokenViewBase):
    permission_classes = [AllowAny]
    serializer_class = TokenCreateSerializer

    def post(self, request: Request, *args, **kwargs) -> Response:
        # try:
        serializer: TokenCreateSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get(EMAIL)
        password = serializer.validated_data.get(PASSWORD)
        user: User | None = authenticate(
            request=request, username=email, password=password
        )
        if not user:
            raise AuthenticationFailed(
                detail=TOKEN_CREATE_AUTHENTICATION_FAILED_FOR_USER(
                    email=email, password=password
                ),
                code="authentication_failed",
            )
        refresh = RefreshToken.for_user(user)
        data = {"access": str(refresh.access_token), "refresh": str(refresh)}
        response_serializer = TokenSerializer(data=data)
        response_serializer.is_valid(raise_exception=True)
        return Response(
            data=response_serializer.validated_data, status=status.HTTP_200_OK
        )
    # except (TokenError, AuthenticationFailed, ValidationError) as exception:
    #     return Response(data=str(exception), status=status.HTTP_400_BAD_REQUEST)


class TokenRefreshView(jwt_views.TokenViewBase):
    serializer_class = RefreshTokenSerializer
    permission_classes = [AllowAny]

    def post(self, request: Request, *args, **kwargs) -> Response:
        try:
            serializer: RefreshTokenSerializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            refresh: RefreshToken = RefreshToken(
                serializer.validated_data.get("refresh")
            )
            if jwt_settings.ROTATE_REFRESH_TOKENS:
                refresh.set_jti()
                refresh.set_exp()
            data = {
                "access": refresh.access_token.__str__(),
                "refresh": refresh.__str__(),
            }
            response_serializer = TokenSerializer(data=data)
            response_serializer.is_valid(raise_exception=True)
            return Response(
                data=response_serializer.validated_data,
                status=status.HTTP_200_OK,
            )
        except (TokenError, ValidationError) as exception:
            return Response(
                data={"error": exception.args},
                status=status.HTTP_400_BAD_REQUEST,
            )
