from rest_framework.permissions import BasePermission
from users.models import CustomUser

class IsDoctor(BasePermission):
    """
    Permission to allow access only to users with the 'doctor' role.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == CustomUser.DOCTOR
