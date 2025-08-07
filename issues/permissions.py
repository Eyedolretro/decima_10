from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Projet

class IsContributorOrProjectOwner(BasePermission):
    """
    Permission : seul un contributeur ou le chef du projet peut accéder aux issues
    """

    def _is_contributor_or_owner(self, user, project):
        return (
            user == project.chef_projet
            or project.collaborateurs.filter(id=user.id).exists()
        )

    def has_permission(self, request, view):
        # DRF gère déjà 401 si pas authentifié
        if not request.user or not request.user.is_authenticated:
            return False

        # Cas particulier pour POST (création d'une issue)
        if request.method == "POST":
            project_id = request.data.get("project")
            if not project_id:
                return False
            try:
                project = Projet.objects.get(id=project_id)
            except Projet.DoesNotExist:
                return False
            return self._is_contributor_or_owner(request.user, project)

        # Pour toutes les autres méthodes, on ne vérifie rien ici
        # → la méthode has_object_permission sera appelée plus tard
        return True

    def has_object_permission(self, request, view, obj):
        # obj peut être soit une issue soit un projet
        if hasattr(obj, "project"):  # Issue
            project = obj.project
        else:  # Projet
            project = obj

        return self._is_contributor_or_owner(request.user, project)


class IsAuthorOrReadOnly(BasePermission):
    """
    Permission : lecture autorisée à tous, modification seulement à l'auteur
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return getattr(obj, 'created_by', None) == request.user
