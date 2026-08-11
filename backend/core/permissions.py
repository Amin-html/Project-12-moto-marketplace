from rest_framework import permissions


class IsSellerOrReadOnly(permissions.BasePermission):
    """
    Читать (GET) может кто угодно, включая анонимов.
    Создавать/менять/удалять — только verified seller или admin.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if not request.user.is_authenticated:
            return False

        if request.user.role == 'admin':
            return True

        if request.user.role == 'seller':
            return hasattr(request.user, 'seller_profile') and request.user.seller_profile.is_verified

        return False

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if obj.seller != request.user and request.user.role != 'admin':
            return False

        if request.user.role == 'seller':
            return hasattr(request.user, 'seller_profile') and request.user.seller_profile.is_verified

        return True