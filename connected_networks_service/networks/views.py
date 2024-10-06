from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from networks.models import ConnectedNetwork
from networks.serializers import ConnectedNetworkSerializer


class ConnectedNetworkViewSet(viewsets.ModelViewSet):
    serializer_class = ConnectedNetworkSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return ConnectedNetwork.objects.filter(user_id=self.request.user.id)