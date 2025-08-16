from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Projet, Issue, Comment

# Users
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

# Projets
class ProjetSerializer(serializers.ModelSerializer):
    chef_projet = UserSerializer(read_only=True)
    collaborateurs_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        source='collaborateurs',
        queryset=User.objects.all(),
        write_only=True
    )

    class Meta:
        model = Projet
        fields = ['id', 'nom', 'description', 'type', 'date_debut', 'date_fin', 'chef_projet', 'collaborateurs_ids']

# Issues
class IssueSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    project = serializers.SerializerMethodField()

    class Meta:
        model = Issue
        fields = ['id', 'title', 'description', 'project', 'created_by', 'priority', 'status']

    def get_project(self, obj):
        if obj.project:
            return {"id": obj.project.id, "nom": obj.project.nom, "type": obj.project.type}
        return None

# Comments
class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    issue = serializers.PrimaryKeyRelatedField(queryset=Issue.objects.all())

    class Meta:
        model = Comment
        fields = ['id', 'text', 'created_at', 'author', 'issue']

    def get_author(self, obj):
        if obj.author:
            return {
                "id": obj.author.id,
                "username": obj.author.username,
                "email": obj.author.email
            }
        return None

    def get_issue(self, obj):
        if obj.issue:
            return {
                "id": obj.issue.id,
                "title": obj.issue.title,
                "project": {"id": obj.issue.project.id, "nom": obj.issue.project.nom} if obj.issue.project else None
            }
        return None
