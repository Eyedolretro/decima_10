from rest_framework import viewsets, generics, permissions, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .serializers import UserSerializer, ProjetSerializer, IssueSerializer, CommentSerializer
from .permissions import IsAuthorOrAdmin
from .controllers import ProjetController, IssueController, CommentController
from .models import Projet


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
    serializer_class = ProjetSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrAdmin]

    def get_queryset(self):
        return ProjetController.get_projets()

    def perform_create(self, serializer):
        projet = ProjetController.create_projet(self.request.user, **serializer.validated_data)
        serializer.instance = projet


# -----------------------
# Issues
# -----------------------
class IssueViewSet(viewsets.ModelViewSet):
    serializer_class = IssueSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrAdmin]

    def get_queryset(self):
        return IssueController.get_issues(self.kwargs.get("projet_pk"))

    def perform_create(self, serializer):
        issue = IssueController.create_issue(
            projet_id=self.kwargs.get("projet_pk"),
            user=self.request.user,
            **serializer.validated_data
        )
        serializer.instance = issue


# -----------------------
# Comments
# -----------------------
class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrAdmin]

    def get_queryset(self):
        return CommentController.get_comments(
            projet_id=self.kwargs.get("projet_pk"),
            issue_id=self.kwargs.get("issue_pk"),
        )

    def perform_create(self, serializer):
        comment = CommentController.create_comment(
            issue_id=self.kwargs.get("issue_pk"),
            user=self.request.user,
            **serializer.validated_data
        )
        serializer.instance = comment


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
