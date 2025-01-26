from rest_framework.permissions import BasePermission
from rest_framework import permissions
from .models import *


class IsActivated(BasePermission):
    def has_permission(self, request, view):
        if bool(request.user and
                request.user.is_authenticated and
                request.user.is_active):
            if request.method in permissions.SAFE_METHODS:
                return True
            elif request.user.role != CustomUser.Roles.CUSTOMER:
                return True
        return False


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS or
            request.user and
            request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in permissions.SAFE_METHODS or
            obj.creator == request.user
        )
