from rest_framework import viewsets, generics, permissions
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import Projet, Issue, Comment
from .serializers import UserSerializer, ProjetSerializer, IssueSerializer, CommentSerializer
from .permissions import IsAuthorOrAdmin

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
    queryset = Projet.objects.all()
    serializer_class = ProjetSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrAdmin]

    def perform_create(self, serializer):
        serializer.save(chef_projet=self.request.user)

# -----------------------
# Issues
# -----------------------
class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrAdmin]

    def perform_create(self, serializer):
        projet_id = self.kwargs.get("projet_pk")
        projet = Projet.objects.get(pk=projet_id)
        serializer.save(
            project=projet,
            created_by=self.request.user
        )

    def get_queryset(self):
        projet_id = self.kwargs.get("projet_pk")
        if projet_id:
            return Issue.objects.filter(project_id=projet_id)
        return Issue.objects.all()

# -----------------------
# Comments
# -----------------------
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrAdmin]

    def get_queryset(self):
        projet_id = self.kwargs.get("projet_pk")
        issue_id = self.kwargs.get("issue_pk")

        qs = Comment.objects.all()
        if issue_id:
            qs = qs.filter(issue_id=issue_id, issue__project_id=projet_id)
        elif projet_id:
            qs = qs.filter(issue__project_id=projet_id)
        return qs

    def perform_create(self, serializer):
        issue_id = self.kwargs.get('issue_pk')
        if not issue_id:
            raise ValueError("issue_pk manquant dans l'URL")
        serializer.save(author=self.request.user, issue_id=issue_id)

# -----------------------
# Comments liés à un projet
# -----------------------
class ProjetCommentViewSet(viewsets.ViewSet):
    """
    Liste tous les commentaires liés aux issues d’un projet.
    """
    def list(self, request, projet_pk=None):
        try:
            projet = Projet.objects.get(pk=projet_pk)
        except Projet.DoesNotExist:
            return Response({"detail": "Projet non trouvé"}, status=404)

        # Assure-toi que le nom du ForeignKey dans Issue est 'project'
        comments = Comment.objects.filter(issue__project=projet)
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
# Liste des commentaires (générique)
# -----------------------
class CommentListView(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

# -----------------------
# Test endpoint
# -----------------------
def test_postman(request):
    return JsonResponse({"message": "Hello Postman"})
