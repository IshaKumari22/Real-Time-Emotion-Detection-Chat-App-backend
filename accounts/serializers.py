from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser

class RegisterSerializer(serializers.ModelSerializer):
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'access', 'refresh']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)

        # Generate tokens
        refresh = RefreshToken.for_user(user)
        return {
            'username': user.username,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }
