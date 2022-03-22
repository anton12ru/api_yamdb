from rest_framework import permissions


class AdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (request.user.is_superuser
                or request.user.is_authenticated
                and request.user.is_admin)


class AdminOnlyPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.user.is_superuser
                or request.user.is_authenticated
                and request.user.is_admin)


class AdminModeratoAuthorOrReadOnly(permissions.BasePermission):

    def has_obj_permission(self, request, view, obj):
        return (
            request.user.is_authenticated
            or obj.author == request.user
            or request.user.is_moderator
            or request.user.is_admin or request.user.is_superuser
        )
