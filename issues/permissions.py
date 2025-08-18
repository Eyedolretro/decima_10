from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAuthorOrAdmin(BasePermission):
    """
    Lecture pour tous.
    Modification/suppression réservée :
    - à l’auteur d’un Issue (created_by)
    - au chef_projet d’un Projet
    - à l’auteur d’un Comment
    - ou à un admin
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        user = request.user
        if user.is_staff:
            return True

        if hasattr(obj, "created_by") and obj.created_by == user:
            return True

        if hasattr(obj, "chef_projet") and obj.chef_projet == user:
            return True

        if hasattr(obj, "author") and obj.author == user:
            return True

        return False
