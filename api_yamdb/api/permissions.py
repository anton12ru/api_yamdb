from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    message = "Нужны права администратора"

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
            request.user.is_superuser
            or request.user.is_authenticated
            and request.user.is_admin
        )


class IsAdmin(permissions.BasePermission):
    message = "Нужны права администратора"

    def has_permission(self, request, view):
        return (
            request.user.is_superuser
            or request.user.is_authenticated
            and request.user.is_admin
        )


class IsAdminOrAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
            request.method == "POST"
            and request.user.is_authenticated
            or request.user.is_admin
            or request.user.is_moderator
            or obj.author == request.user
        )
