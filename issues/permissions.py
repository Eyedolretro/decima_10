from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAuthorOrAdmin(BasePermission):
    """
    Lecture pour tous, modification/suppression seulement auteur ou admin
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return getattr(obj, 'created_by', None) == request.user or request.user.is_staff
