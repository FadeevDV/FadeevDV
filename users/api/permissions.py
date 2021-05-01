from django.conf import settings
from rest_framework import permissions

ROLE_CHOICES = settings.ROLE_CHOICES
USER = ROLE_CHOICES[0][0]
MODERATOR = ROLE_CHOICES[1][0]
ADMIN = ROLE_CHOICES[2][0]


class IsAdministrator(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return True
            if request.user.role == ADMIN or request.user.is_staff:
                return True


class IsAuthenticatedUserOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            if request.user.role == USER:
                return True


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            if request.user == obj.author:
                return True
            if request.user.role == MODERATOR:
                return True
