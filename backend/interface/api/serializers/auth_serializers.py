from rest_framework import serializers
from infrastructure.persistence.models import UserRole

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(min_length=3, max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=6)
    role = serializers.ChoiceField(choices=UserRole.choices, required=False)
    phone = serializers.CharField(required=False, allow_blank=True)
    name = serializers.CharField(required=False, allow_blank=True)

class LoginSerializer(serializers.Serializer):
    identifier = serializers.CharField(help_text="username ou email")
    password = serializers.CharField(write_only=True)

class OTPRequestSerializer(serializers.Serializer):
    identifier = serializers.CharField()

class OTPVerifySerializer(serializers.Serializer):
    identifier = serializers.CharField()
    code = serializers.CharField(max_length=6)

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

class PasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.CharField()
    new_password = serializers.CharField(min_length=6)