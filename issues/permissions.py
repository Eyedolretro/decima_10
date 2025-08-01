# issues/permissions.py

from rest_framework.permissions import BasePermission

class IsAuthorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Lecture autorisée pour tout utilisateur connecté
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        # Modification / Suppression seulement pour l'auteur
        return obj.author_user == request.user
