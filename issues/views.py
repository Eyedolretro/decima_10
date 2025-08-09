from rest_framework import viewsets, permissions, generics, status
from django.db import models  # Nécessaire pour Q()
from .models import Issue, Comment, Projet
from .serializers import (
    IssueSerializer,
    CommentSerializer,
    RegisterSerializer,
    ProjetSerializer
)
from django.contrib.auth.models import User
from .permissions import IsAuthorOrReadOnly, IsContributorOrProjectOwner
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response


class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated, IsContributorOrProjectOwner]

    def get_queryset(self):
        user = self.request.user
        return Issue.objects.filter(
            project__collaborateurs=user
        ) | Issue.objects.filter(
            project__chef_projet=user
        )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def perform_create(self, serializer):
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

    def get_queryset(self):
        user = self.request.user
        return Projet.objects.filter(
            models.Q(chef_projet=user) | models.Q(collaborateurs=user)
        ).distinct()

    @action(detail=True, methods=['patch'], url_path='collaborateurs/(?P<user_id>[^/.]+)')
    def update_collaborateur_role(self, request, pk=None, user_id=None):
        projet = self.get_object()
        try:
            collaborateur = projet.collaborateurs.get(id=user_id)
        except projet.collaborateurs.model.DoesNotExist:
            return Response({'detail': 'Collaborateur non trouvé'}, status=status.HTTP_404_NOT_FOUND)

        role = request.data.get('role')
        if role not in ['chef', 'contributeur']:
            return Response({'detail': 'Rôle invalide'}, status=status.HTTP_400_BAD_REQUEST)

        # Utilise le related_name défini dans la classe ProjetCollaborateur (à adapter selon ton modèle)
        relation = projet.collaborateurs_relations.filter(user=collaborateur).first()
        if not relation:
            return Response({'detail': 'Relation collaborateur-projet introuvable'}, status=status.HTTP_404_NOT_FOUND)

        relation.role = role
        relation.save()

        return Response({'detail': f'Rôle de {collaborateur.username} mis à jour en {role}'}, status=status.HTTP_200_OK)
