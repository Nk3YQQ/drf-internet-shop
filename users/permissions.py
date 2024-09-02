from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """ Ограничение на суперпользователя """

    def has_permission(self, request, view):
        return True if request.user.is_superuser else False
