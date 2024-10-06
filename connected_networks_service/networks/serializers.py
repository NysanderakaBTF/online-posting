from rest_framework import serializers

from networks.models import ConnectedNetwork


class ConnectedNetworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConnectedNetwork
        fields = '__all__'