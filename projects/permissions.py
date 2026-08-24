from rest_framework.permissions import BasePermission

from accounts.models import User


class IsClient(BasePermission):
    message = "Only clients can perform this action."

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == User.Role.CLIENT
        )