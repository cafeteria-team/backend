from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from users.models import User


class AdminPermission(BasePermission):
    message = "Permission deniend!"

    def has_permission(self, request, view):
        user_roles = User.UserRoles
        if request.user.role == user_roles.ADMIN:
            return True

        return False
