from django.shortcuts import render
from .models import Product, CustomUser
from rest_framework import generics, permissions
from .serializers import *
from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import logout, update_session_auth_hash
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import permission_classes


class LogInView(generics.GenericAPIView):
    serializer_class = LogInSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)  # Use the serializer class defined above
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = CustomUser.objects.get(username=username, password=password)

            if user is not None and user.is_active:
                refresh = RefreshToken.for_user(user)
                login(request, user)
                return Response({"detail": "Login successful.",
                                 'refresh': str(refresh),
                                 'access': str(refresh.access_token),
                                 }, status=status.HTTP_200_OK)
            elif user is not None and not user.is_active:
                return Response({"detail": "User is not active."}, status=status.HTTP_401_UNAUTHORIZED)
            print(user)
            return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        return Response({"detail": "Please enter your login credentials."})


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"detail": "User created successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        return Response({"detail": "Please enter your registration details."})


class ProductList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]


@permission_classes([permissions.IsAuthenticated])
class UserLogoutApiView(generics.RetrieveAPIView):
    def get(self, *args, **kwargs):
        try:
            logout(self.request)
            return Response({'message': 'Log outed successfully.'})
        except:
            return Response({'status': 400, 'message': 'Something went wrong, please try again'})


@permission_classes([permissions.IsAuthenticated])
class PasswordChangeApiView(generics.GenericAPIView):
    serializer_class = PasswordChangeSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = PasswordChangeSerializer(data=data)
        if serializer.is_valid():
            print(1)
            user = request.user
            if user.check_password(serializer.data.get('old_password')):
                print(2)
                user.set_password(serializer.data.get('new_password'))
                user.save()
                update_session_auth_hash(request, user)
                print(3)
                return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)
            return Response({'error': 'Incorrect old password.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
