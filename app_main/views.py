from drf_spectacular.utils import extend_schema, extend_schema_view
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from app_main.filters import UserProfileFilter
from app_main.models import UserProfile
from app_main.serializers.user_profile import (
    UserProfileDefaultSerializer,
    LoginSerializer,
    SignUpSerializer,
    UserProfileUpdateSerializer
)
from app_main.utils import get_user_login_data, ResponseUtils
from rideapi.permissions import TokenAndRolePermission, TokenAuthenticationPermission


@extend_schema(tags=['User'])
@extend_schema_view()
class ProfileView(viewsets.GenericViewSet):
    permission_classes = [TokenAndRolePermission]
    required_role = ['R001']
    filter_backends = (UserProfileFilter,)
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileDefaultSerializer
    action_serializers = {
        'login': LoginSerializer,
        'signup': SignUpSerializer,
        'profile_update': UserProfileUpdateSerializer,
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
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            response_data = get_user_login_data(instance['id'])
            return Response(response_data)

        return ResponseUtils.error_response(serializer.errors)

    @action(
        detail=False,
        methods=['post'],
        permission_classes=[AllowAny],
        url_path='create'
    )
    def signup(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return ResponseUtils.error_response(serializer.errors)

        data = serializer.save()
        response_message = data.get('message')
        if not data.get('success'):
            return ResponseUtils.error_response(response_message, error=data.get('error'))

        return ResponseUtils.success_response(response_message)


    @action(
        detail=False,
        methods=['patch'],
        permission_classes=[TokenAuthenticationPermission],
        url_path='<int:id>/update'
    )
    def profile_update(self, request, id):
        user_profile = UserProfile.objects.filter(id=id).first()
        if not user_profile:
            return ResponseUtils.error_response('User profile not found!')

        serializer = self.get_serializer(user_profile, data=request.data)
        if not serializer.is_valid():
            return ResponseUtils.error_response(serializer.errors)

        data = serializer.save()
        response_message = data.get('message')
        if not data.get('success'):
            return ResponseUtils.error_response(response_message, error=data.get('error'))

        profile = UserProfileDefaultSerializer(user_profile)
        return ResponseUtils.success_response(response_message, data=profile.data)


    @action(
        detail=False,
        methods=['delete'],
        permission_classes=[TokenAndRolePermission],
        url_path='<int:id>/remove'
    )
    def delete(self, request, id):
        try:
            user_profile = UserProfile.objects.filter(id=id).first()
            if not user_profile:
                return ResponseUtils.error_response('User profile not found!')

            user_profile.is_deleted = True
            user_profile.save()

            response_message = 'Successfully deleted!'
            return ResponseUtils.success_response(response_message)

        except Exception as e:
            response_message = 'Unable to process at this moment!'
            return ResponseUtils.error_response(response_message, error=str(e))
