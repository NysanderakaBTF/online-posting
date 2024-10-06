import uuid

import requests
from django.conf import settings
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

class JWTAuthenticationMiddleware(MiddlewareMixin):
    def __init__(self, get_response=None):
        self.get_response = get_response
        self.user_service_url = settings.USER_SERVICE_URL

    def process_request(self, request):
        excluded_paths = getattr(settings, 'AUTH_EXCLUDED_PATHS', [])
        if request.path in excluded_paths:
            return None

        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return JsonResponse({'detail': 'Authentication credentials were not provided.'}, status=401)

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
            return JsonResponse({'detail': 'Authentication service unavailable.'}, status=503)

        if response.status_code != 200:
            return JsonResponse({'detail': 'Invalid token.'}, status=401)

        try:
            response = requests.get(
                f'{self.user_service_url}/auth/user/',
                headers={'Authorization': f'Bearer {token}'},
                timeout=5
            )
        except requests.exceptions.RequestException:
            return JsonResponse({'detail': 'Authentication service unavailable.'}, status=503)


        user_data = response.json()
        user_data.setdefault('is_authenticated', True)
        request.user = user_data
        return None