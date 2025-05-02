from rest_framework.permissions import BasePermission


class IsNotAdminUser(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and not request.user.is_staff


class CategoryPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == "GET":
            return True
        else:
            return request.user.is_staff


