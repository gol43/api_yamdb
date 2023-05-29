from rest_framework import permissions
from reviews.models import User


class AdminPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and (request.user.is_superuser
                     or request.user.role == User.RoleChoices.ADMIN))


class AdminAndRead(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS or (
            request.user.is_authenticated and (
                request.user.is_superuser
                or request.user.role == User.RoleChoices.ADMIN)))


class ForAllAndRead(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.role == User.RoleChoices.ADMIN
            or request.user.role == User.RoleChoices.MODERATOR)
