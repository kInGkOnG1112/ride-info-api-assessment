from rest_framework import permissions, authentication, exceptions

from app_main.models import UserProfile


class BaseTokenPermission(authentication.BaseAuthentication):
    """
    Base permission to check token authentication.
    """

    def has_permission(self, request, view):
        if not request.__dict__.get("_user").is_authenticated:
            raise exceptions.NotAuthenticated({
                "statusCode": 401,
                "message": "Authentication credentials were not provided.",
                "is_token_expired": False
            })
        return True

    def authenticate_header(self, request):
        return 'Bearer'


class TokenAuthenticationPermission(BaseTokenPermission):
    """
    Permission to check only token authentication.
    """
    pass


class TokenAndRolePermission(BaseTokenPermission, permissions.BasePermission):
    """
    Permission to check token authentication and user's role.
    """

    def has_permission(self, request, view):
        # First, check token authentication
        if not super().has_permission(request, view):
            return False

        # Then, check the user's role
        required_role = getattr(view, 'required_role', None)
        user_profile = UserProfile.objects.get(user=request.user)
        if required_role and user_profile.role.code not in required_role:
            raise exceptions.PermissionDenied({
                "status_code": 403,
                "message": "You do not have permission to perform this action.",
            })

        return True
