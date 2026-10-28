from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["id", "name", "email", "password"]

    def validate_email(self, v):
        v = v.lower()
        if User.objects.filter(email=v).exists():
            raise serializers.ValidationError("This email is already registered")
        return v

    def validate_password(self, v):
        validate_password(v)
        return v

    def create(self, data):
        return User.objects.create_user(**data)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, d):
        u = authenticate(
            request=self.context.get("request"),
            email=d["email"].lower(),
            password=d["password"],
        )
        if u is None:
            raise AuthenticationFailed("Invalid email or password")
        d["user"] = u
        return d
