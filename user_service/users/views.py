from rest_framework import viewsets, status, permissions
from rest_framework.response import Response

from users.models import User
from users.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    def destroy(self, request, *args, **kwargs):
        if request.user.is_authenticated and (request.user.id == int(kwargs['pk']) or request.user.is_admin):
            return super().destroy(request, *args, **kwargs)
        return Response(status=status.HTTP_403_FORBIDDEN)
    def retrieve(self, request, *args, **kwargs):
        if request.user.is_authenticated and (request.user.id == int(kwargs['pk']) or request.user.is_admin):
            return super().retrieve(request, *args, **kwargs)
        return Response(status=status.HTTP_403_FORBIDDEN)
    def update(self, request, *args, **kwargs):
        if request.user.is_authenticated and (request.user.id == int(kwargs['pk']) or request.user.is_admin):
            return super().update(request, *args, **kwargs)
        return Response(status=status.HTTP_403_FORBIDDEN)
