from django.db import models
from django.contrib.auth.models import User

class Issue(models.Model):
    STATUS_CHOICES = [
        ('open', 'Ouvert'),
        ('in_progress', 'En cours'),
        ('closed', 'Fermé'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Basse'),
        ('medium', 'Moyenne'),
        ('high', 'Haute'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='issues')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Commentaire sur {self.issue.title} par {self.author.username}"
