from django.shortcuts import render
from .models import Product
from rest_framework import generics, permissions
from .serializers import *
from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from rest_framework import status
from store import settings

class LoginView(generics.GenericAPIView):
    serializer_class = LogInSerializer
    def post(self, request, *args, **kwargs):
        serializer = LogInSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = CustomUser.objects.filter(username=username, password=password).first()
            if user is not None:
                login(request, user)
                return Response({"detail": "Login successful."}, status=status.HTTP_200_OK)
            return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, *args, **kwargs):
        return Response({"Введите свои данные для входа в аккаунт"})

class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "User created successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, *args, **kwargs):
        return Response({"Введите свои данные для регистрации в аккаунт"})

class ProductList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
