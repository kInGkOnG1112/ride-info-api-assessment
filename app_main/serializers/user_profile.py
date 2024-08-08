from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import transaction
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

    def validate(self, data):
        errors = dict()
        username = data['username']
        password = data['password']

        authenticated_user = authenticate(username=username, password=password)
        if not authenticated_user:
            errors['generic'] = 'Account not found.'

        if errors:
            raise serializers.ValidationError(errors)
        return data

    def save(self, **kwargs):
        data = save_validated_data(self.validated_data.items(), kwargs.items())
        username = data['username']
        user = User.objects.get(username=username)
        return {'id': user.id}



class SignUpSerializer(serializers.Serializer):

    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    email = serializers.CharField(max_length=50)
    phone_number = serializers.CharField(max_length=20)
    role = serializers.CharField(max_length=10)
    password = serializers.CharField(max_length=20)
    confirm_password = serializers.CharField(max_length=20)

    class Meta:
        fields = '__all__'

    def validate(self, data):
        errors = dict()
        email = data.get('email', '').strip()

        try:
            validate_email(email)
        except ValidationError:
            errors['email'] = 'Invalid email format.'

        if email:
            if User.objects.filter(email=email).exists():
                errors['email'] = 'Email address is no longer available.'

        if data.get('password') != data.get('confirm_password'):
            errors['password'] = 'The password confirmation does not match.'

        if not Role.objects.filter(code=data.get('role')).exists():
            errors['role'] = 'Role does not exist.'

        if errors:
            raise serializers.ValidationError(errors)
        return data

    def save(self, **kwargs):
        try:
            data = save_validated_data(self.validated_data.items(), kwargs.items())
            email = data.get('email')
            password = data.get('confirm_password')

            with transaction.atomic():
                user = User.objects.create_user(
                    username=email,
                    email=email,
                    first_name=data.get('first_name'),
                    last_name=data.get('last_name'),
                )
                user.set_password(password)
                user.save()

                role = Role.objects.get(code=data.get('role'))
                UserProfile.objects.create(
                    role=role,
                    user=user,
                    phone_number=data.get('phone_number'),
                )
                return {
                    'success': True,
                    'message': 'Successfully registered.',
                }

        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'Unable to process at this moment!'
            }
