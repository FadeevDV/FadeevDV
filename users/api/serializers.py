from rest_framework import serializers

from users.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'first_name', 'last_name', 'username', 'bio', 'email', 'role'
        )
        model = CustomUser


class CreateUserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('email', 'username')
        model = CustomUser
