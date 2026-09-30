from rest_framework.permissions import BasePermission

class IsAdminProfile(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user.is_authenticated
            and (request.user.is_staff or getattr(getattr(request.user, "profile", None), "role", "") == "admin")
        )
