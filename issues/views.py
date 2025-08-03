from rest_framework import viewsets, permissions, generics
from django.db import models  # Nécessaire pour Q()
from .models import Issue, Comment, Projet
from .serializers import (
    IssueSerializer,
    CommentSerializer,
    RegisterSerializer,
    ProjetSerializer
)
from django.contrib.auth.models import User
from .permissions import IsAuthorOrReadOnly,IsContributorOrProjectOwner
from rest_framework.permissions import IsAuthenticated




class IssueViewSet(viewsets.ModelViewSet):
    """
    CRUD sur les Issues
    - Seuls les contributeurs ou le chef du projet peuvent créer, lire, modifier, supprimer
    """
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated, IsContributorOrProjectOwner]

    def perform_create(self, serializer):
        """
        Associe automatiquement l'utilisateur connecté comme 'created_by'
        """
        serializer.save(created_by=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# Inscription utilisateur
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer


class ProjetViewSet(viewsets.ModelViewSet):
    queryset = Projet.objects.all()
    serializer_class = ProjetSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(chef_projet=self.request.user)
