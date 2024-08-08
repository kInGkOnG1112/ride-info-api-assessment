
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from app_main.models import UserProfile


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def get_user_login_data(user_id):
    """
    Retrieves user data after a successful login
    :param user_id:
    :return:
    """

    from app_main.serializers.user_profile import UserProfileDefaultSerializer

    user_login_data = {}
    user = User.objects.get(pk=user_id)
    profile = UserProfile.objects.get(user=user)
    user_login_data.update({"profile":  UserProfileDefaultSerializer(profile).data})
    user_login_data['token'] = get_tokens_for_user(user)

    return user_login_data


def save_validated_data(data_list, kwarg_list):
    """
    Return dictionary of validated data in base serializer save method
    """
    return dict(list(data_list) + list(kwarg_list))


class ResponseUtils:
    """
    Response Utility
    """

    @staticmethod
    def _construct_response(message, data=None, error=None, status_code=status.HTTP_200_OK):
        response = {
            'status_code': status_code,
            'message': message
        }
        if data is not None:
            response['data'] = data
        if error is not None:
            response['error'] = error

        return Response(response, status=status_code)

    @staticmethod
    def success_response(message, data=None, status_code=status.HTTP_200_OK):
        return ResponseUtils._construct_response(message, data=data, status_code=status_code)

    @staticmethod
    def error_response(message, error=None, status_code=status.HTTP_400_BAD_REQUEST):
        return ResponseUtils._construct_response(message, error=error, status_code=status_code)
