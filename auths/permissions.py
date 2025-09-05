from rest_framework.permissions import BasePermission


class APIPermission(BasePermission):
    allow_read_only = False
    
    @staticmethod
    def is_safe(request) -> bool:
        return request.method in ["GET", "HEAD", "OPTIONS"]

class IsAdminUser(APIPermission):

    def has_permission(self, request, view) -> bool:
        return request.user and getattr(__o=request.user, __name="is_admin", __default=False)

    def has_object_permission(self, request, view, obj) -> bool:
        return super().has_object_permission(request, view, obj)


class AllowAny(APIPermission):

    def has_permission(self, request, view) -> bool:
        return True

    def has_object_permission(self, request, view, obj):
        return True


class IsAuthenticatedUser(APIPermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return super().has_object_permission(request, view, obj)
