from datetime import timedelta

from django.utils import timezone
from django.utils.functional import SimpleLazyObject
from django.contrib.auth.middleware import get_user
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication


def get_user_jwt(request: Request):
    user = get_user(request)
    if user.is_authenticated:
        return user
    try:
        user_jwt = JWTAuthentication().authenticate(Request(request))
        if user_jwt is not None:
            return user_jwt[0]
    except:
        pass
    return user


class AuthenticationMiddlewareJWT:
    def __init__(self, get_response) -> None:
        self.get_response = get_response

    def __call__(self, request):
        request.user = SimpleLazyObject(lambda: get_user_jwt(request))
        response = self.get_response(request)
        return response


class UserActivityMiddleware:
    def __init__(self, get_response) -> None:
        self.get_response = get_response

    def __call__(self, request: Request) -> Response:
        user = request.user
        if user.is_authenticated:
            last_active = user.last_active
            current = timezone.now()
            if not last_active or last_active <= current - timedelta(
                minutes=3
            ):
                user.last_active = current
                user.save()
        response = self.get_response(request)
        return response
