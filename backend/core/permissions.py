from rest_framework import permissions

class IsSellerOrReadOnly(permissions.BasePermission):
    """
    Читать (GET) может кто угодно, включая анонимов.
    Создавать/менять/удалять — только seller или admin.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            # SAFE_METHODS = GET, HEAD, OPTIONS — то, что не меняет данные
            return True
        return request.user.is_authenticated and request.user.role in ['seller', 'admin']

    def has_object_permission(self, request, view, obj):
        # проверка уже на конкретный объект — можно ли МЕНЯТЬ ИМЕННО ЭТОТ товар
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.seller == request.user or request.user.role == 'admin'
        # свой товар редактировать можно, чужой — только если ты admin