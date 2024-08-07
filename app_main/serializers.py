from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers

from app_main.models import (
    UserProfile,
    Role
)
from app_main.utils import save_validated_data


class UserDefaultSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'is_superuser')


class RoleDefaultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'


class UserProfileDefaultSerializer(serializers.ModelSerializer):
    user = UserDefaultSerializer()
    role = RoleDefaultSerializer()

    class Meta:
        model = UserProfile
        fields = '__all__'


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        model = UserProfile
        fields = ('username', 'password')

    def validate(self, attrs):
        errors = dict()
        username = attrs['username']
        password = attrs['password']

        authenticated_user = authenticate(username=username, password=password)
        if not authenticated_user:
            errors['generic'] = 'Account not found.'

        if errors:
            raise serializers.ValidationError(errors)
        return attrs

    def save(self, **kwargs):
        data = save_validated_data(self.validated_data.items(), kwargs.items())
        username = data['username']
        user = User.objects.get(username=username)
        return {'id': user.id}
