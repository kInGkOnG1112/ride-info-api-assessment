from django.shortcuts import render
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from app_main.models import UserProfile
from app_main.serializers import (
    UserProfileDefaultSerializer,
    LoginSerializer
)
from app_main.utils import get_user_login_data, ResponseUtils


@extend_schema(tags=['Profile'])
@extend_schema_view()
class ProfileView(viewsets.GenericViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileDefaultSerializer
    action_serializers = {
        'login': LoginSerializer
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
        """
        Health Condition List
        """
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
