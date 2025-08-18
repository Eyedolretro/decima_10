from django.contrib.auth.models import User
from .models import Projet, Issue, Comment


class ProjetController:
    @staticmethod
    def create_projet(user, **validated_data):
        return Projet.objects.create(chef_projet=user, **validated_data)

    @staticmethod
    def get_projets():
        return Projet.objects.all()


class IssueController:
    @staticmethod
    def create_issue(projet_id, user, **validated_data):
        projet = Projet.objects.get(pk=projet_id)
        return Issue.objects.create(
            project=projet,
            created_by=user,
            **validated_data
        )

    @staticmethod
    def get_issues(projet_id=None):
        if projet_id:
            return Issue.objects.filter(project_id=projet_id)
        return Issue.objects.all()


class CommentController:
    @staticmethod
    def create_comment(issue_id, user, **validated_data):
        return Comment.objects.create(
            issue_id=issue_id,
            author=user,
            **validated_data
        )

    @staticmethod
    def get_comments(projet_id=None, issue_id=None):
        qs = Comment.objects.all()
        if issue_id:
            qs = qs.filter(issue_id=issue_id, issue__project_id=projet_id)
        elif projet_id:
            qs = qs.filter(issue__project_id=projet_id)
        return qs

    @staticmethod
    def get_comments_by_projet(projet_id):
        return Comment.objects.filter(issue__project_id=projet_id)
