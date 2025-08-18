from rest_framework import viewsets, generics, permissions
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.http import JsonResponse
from .serializers import UserSerializer, ProjetSerializer, IssueSerializer, CommentSerializer
from .permissions import IsAuthorOrAdmin
from .controllers import ProjetController, IssueController, CommentController


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
# Endpoint test
# -----------------------
def test_postman(request):
    return JsonResponse({"message": "Hello Postman"})
