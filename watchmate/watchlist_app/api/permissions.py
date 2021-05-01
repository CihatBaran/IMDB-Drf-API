from rest_framework import permissions


class AdminOrReadOnly(permissions.IsAdminUser):
    """
    Check superuser has permission 
    """

    def has_permission(self, request, view):
        """
        Check the user is admin or not to make anything other than fetching data
        """
        admin_permission = bool(
            request.user and request.user.is_staff and request.user.is_superuser)

        if request.method in permissions.SAFE_METHODS:
            return True
        return admin_permission


class StaffAdminOrReadOnly(permissions.IsAdminUser):
    """
    Check the user is staff and permission to change the data
    """

    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        if request.method in permissions.SAFE_METHODS:
            return True

        staff_permission = bool(request.user and request.user.is_staff)
        return staff_permission


class ReviewUserOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        should_grant = obj.review_user == request.user

        if request.method in permissions.SAFE_METHODS:
            return True

        if should_grant or request.user.is_superuser:
            return True
        else:
            return False
