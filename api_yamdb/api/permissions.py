from rest_framework import permissions


class AdminOrReadOnlyPermission(permissions.BasePermission):
    '''Доступ для чтения всем'''
    def has_object_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff


class AdminOnlyPermission(permissions.BasePermission):
    '''доступ только аутентифицированным пользователям'''
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_admin or request.user.is_staff)

    def has_object_permission(self, request, view):
        return request.user.is_authenticated and(
            request.user.is_admin or request.user.is_staff
        )


class IsAdminModeratorOwnerOrReadOnly(permissions.BasePermission):
    '''Доступ для чтения всем, редактировать могут: Админы и владельцы'''
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or (
            request.user.is_authenticated and (
                request.user.is_moderator or request.user.is_admin
            )
        )

    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS or (
            request.user.is_authenticated and (
            obj.author == request.user
            or request.user.is_moderator
            or request.user.is_admin
            )
        )
