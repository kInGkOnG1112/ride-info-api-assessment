from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from app_main.models import UserProfile
from app_main.serializers.user_profile import (
    UserProfileDefaultSerializer,
    LoginSerializer,
    SignUpSerializer
)
from app_main.utils import get_user_login_data, ResponseUtils
from rideapi.permissions import TokenAndRolePermission, TokenAuthenticationPermission


@extend_schema(tags=['User'])
@extend_schema_view()
class ProfileView(viewsets.GenericViewSet):
    permission_classes = [TokenAndRolePermission]
    required_role = ['R001']
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileDefaultSerializer
    action_serializers = {
        'login': LoginSerializer,
        'signup': SignUpSerializer,
    }

    def get_serializer_class(self):
        """
        Retrieve the appropriate serializer for every request method
        """
        if hasattr(self, 'action_serializers'):
            if self.action in self.action_serializers:
                return self.action_serializers[self.action]

        return super(ProfileView, self).get_serializer_class()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        paginated = request.GET.get('paginated', 'true')

        if paginated == 'true':
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(
        detail=False,
        methods=['post'],
        url_path='login',
        permission_classes=[AllowAny]
    )
    def login(self, request, *args, **kwargs):
        """
        User Login
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            response_data = get_user_login_data(instance['id'])
            return Response(response_data)

        return ResponseUtils.error_response(serializer.errors)

    @action(
        detail=False,
        methods=['post'],
        permission_classes=[AllowAny]
    )
    def signup(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            data = serializer.save()
            response_message = data.get('message')
            if data.get('success'):
                return ResponseUtils.success_response(response_message)
            return ResponseUtils.error_response(response_message, error=data.get('error'))
        return ResponseUtils.error_response(serializer.errors)
