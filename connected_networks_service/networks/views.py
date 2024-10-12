from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from networks.models import ConnectedNetwork
from networks.serializers import ConnectedNetworkSerializer

@method_decorator(csrf_exempt, name='dispatch')
class ConnectedNetworkViewSet(viewsets.ModelViewSet):
    serializer_class = ConnectedNetworkSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return ConnectedNetwork.objects.filter(user_id=self.request.user.id)