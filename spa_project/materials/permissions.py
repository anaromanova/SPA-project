from rest_framework import permissions

class NotModeratorCannotModify(permissions.BasePermission):
    """
    Пользователи в группе 'moderators' могут читать и править,
    но не могут создавать (POST) и удалять (DELETE) материалы и уроки.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.groups.filter(name='moderators').exists() and request.method in ('POST', 'DELETE'):
            return False

        return True

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Позволяет владельцу (obj.user) читать и менять,
    остальным — только читать (SAFE_METHODS).
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user
