import requests
from django.conf import settings
from rest_framework import authentication
from rest_framework.response import Response
from rest_framework import exceptions

from authentication.user import CustomUser


class JWTMicroserviceAuthenticator(authentication.BaseAuthentication):
    def __init__(self):
        self.user_service_url = settings.USER_SERVICE_URL

    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None

        if not auth_header.startswith('Bearer '):
            raise exceptions.AuthenticationFailed('Authentication credentials were not provided.')

        token = auth_header[7:]

        try:
            response = requests.post(
                f'{self.user_service_url}/auth/token/verify/',
                headers={'Authorization': f'Bearer {token}'},
                timeout=5,
                data={
                    'token':token
                }
            )
        except requests.exceptions.RequestException:
            raise exceptions.AuthenticationFailed('Authentication service unavailable')

        if response.status_code != 200:
            raise exceptions.AuthenticationFailed('Token Invalid')

        try:
            response = requests.get(
                f'{self.user_service_url}/auth/user/',
                headers={'Authorization': f'Bearer {token}'},
                timeout=5
            )
        except requests.exceptions.RequestException:
            raise exceptions.APIException({'detail': 'Authentication service unavailable.'}, code=503)

        user_data = response.json()
        if user_data:
            user = CustomUser(user_data)
            return (user, token)
        else:
            return (None, None)