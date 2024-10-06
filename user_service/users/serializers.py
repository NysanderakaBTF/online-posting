from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password', 'balance', 'is_admin']
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)