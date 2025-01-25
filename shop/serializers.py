from rest_framework import serializers
from rest_framework.serializers import CurrentUserDefault, HiddenField
from django.contrib.auth.hashers import make_password
from .models import *


class LogInSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', "password", 'email', 'telegram_id']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        user = CustomUser(**validated_data)
        user.save()
        return user


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class ProductSerializer(serializers.ModelSerializer):
    creator = HiddenField(default=CurrentUserDefault())
    price = serializers.IntegerField()

    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'quantity', 'category', 'creator']

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be a positive integer.")
        return value
