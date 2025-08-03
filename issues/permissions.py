from rest_framework.permissions import BasePermission
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

        # Pour POST (création d'une issue), on doit vérifier sur le projet
        if request.method == "POST":
            project_id = request.data.get("project")
            if not project_id:
                return False
            try:
                project = Projet.objects.get(id=project_id)
            except Projet.DoesNotExist:
                # Projet inexistant → l'URL est valide mais l'objet pas trouvé → 404
                return False
            return self._is_contributor_or_owner(request.user, project)

        # Pour GET, PUT, DELETE → DRF appellera has_object_permission
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