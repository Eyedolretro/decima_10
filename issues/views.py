from rest_framework import viewsets, generics, permissions, status
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .serializers import UserSerializer, ProjetSerializer, IssueSerializer, CommentSerializer
from .permissions import IsAuthorOrAdmin
from .controllers import ProjetController, IssueController, CommentController
from .models import Projet
from rest_framework.decorators import action



# -----------------------
# Users
# -----------------------
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        if request.user != user and not request.user.is_staff:
            return Response({"detail": "Permission denied"}, status=403)
        return super().destroy(request, *args, **kwargs)


# -----------------------
# Projets
# -----------------------
class ProjetViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les projets.

    list:
    Retourne la liste de tous les projets accessibles à l'utilisateur.

    retrieve:
    Retourne les détails d'un projet spécifique.

    create:
    Crée un nouveau projet.

    update:
    Met à jour un projet existant.

    partial_update:
    Met à jour partiellement un projet.

    destroy:
    Supprime un projet.
    """
    queryset = Projet.objects.all()
    serializer_class = ProjetSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['get'])
    def collaborateurs(self, request, pk=None):
        """
        Retourne la liste des collaborateurs d'un projet.
        """
        projet = self.get_object()
        serializer = ProjetCollaborateurSerializer(projet.collaborateurs, many=True)
        return Response(serializer.data)
# -----------------------
# Issues
# -----------------------
class IssueViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les issues liées aux projets.

    list:
    Retourne la liste des issues pour un projet donné.

    retrieve:
    Retourne les détails d'une issue spécifique.

    create:
    Crée une nouvelle issue pour un projet.

    update:
    Met à jour une issue existante.

    partial_update:
    Met à jour partiellement une issue.

    destroy:
    Supprime une issue.
    """
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Retourne les issues filtrées par projet.
        """
        projet_id = self.kwargs.get('projet_pk')
        return Issue.objects.filter(projet_id=projet_id)


# -----------------------
# Comments
# -----------------------
class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les commentaires sur les issues.

    list:
    Retourne tous les commentaires d'une issue.

    retrieve:
    Retourne les détails d'un commentaire spécifique.

    create:
    Crée un commentaire pour une issue.

    update:
    Met à jour un commentaire existant.

    partial_update:
    Met à jour partiellement un commentaire.

    destroy:
    Supprime un commentaire.
    """
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Retourne les commentaires filtrés par issue et projet.
        """
        issue_id = self.kwargs.get('issue_pk')
        return Comment.objects.filter(issue_id=issue_id)


# -----------------------
# Comments liés à un projet
# -----------------------
class ProjetCommentViewSet(viewsets.ViewSet):
    def list(self, request, projet_pk=None):
        comments = CommentController.get_comments_by_projet(projet_pk)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)


# -----------------------
# Register
# -----------------------
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


# -----------------------
# Collaborateurs d'un projet
# -----------------------
class ProjetCollaborateurViewSet(viewsets.ViewSet):
    """
    Gestion des collaborateurs d'un projet.
    """

    def list(self, request, projet_pk=None):
        projet = get_object_or_404(Projet, pk=projet_pk)
        if not hasattr(projet, "collaborateurs"):
            return Response(
                {"error": "Ce projet n'a pas de collaborateurs définis."},
                status=status.HTTP_400_BAD_REQUEST
            )
        collaborateurs = projet.collaborateurs.all()
        serializer = UserSerializer(collaborateurs, many=True)
        return Response(serializer.data)

    def create(self, request, projet_pk=None):
        projet = get_object_or_404(Projet, pk=projet_pk)
        if not hasattr(projet, "collaborateurs"):
            return Response(
                {"error": "Ce projet ne peut pas avoir de collaborateurs."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user_id = request.data.get("user_id")
        if not user_id:
            return Response({"error": "user_id requis"}, status=400)

        user = get_object_or_404(User, pk=user_id)
        projet.collaborateurs.add(user)
        return Response({"message": "Collaborateur ajouté"}, status=201)

    def destroy(self, request, pk=None, projet_pk=None):
        projet = get_object_or_404(Projet, pk=projet_pk)
        if not hasattr(projet, "collaborateurs"):
            return Response(
                {"error": "Ce projet n'a pas de collaborateurs à supprimer."},
                status=status.HTTP_400_BAD_REQUEST
            )
        user = get_object_or_404(User, pk=pk)
        projet.collaborateurs.remove(user)
        return Response({"message": "Collaborateur supprimé"}, status=204)


# -----------------------
# Endpoint test
# -----------------------
def test_postman(request):
    return JsonResponse({"message": "Hello Postman"})
