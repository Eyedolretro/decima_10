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

    project = models.ForeignKey(
        'Projet',
        on_delete=models.CASCADE,
        related_name='issues',
        null=True,
        blank=True
    )

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


class Projet(models.Model):
    TYPE_CHOICES = [
        ('backend', 'Back-end'),
        ('frontend', 'Front-end'),
        ('ios', 'iOS'),
        ('android', 'Android'),
    ]

    nom = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    date_debut = models.DateField(null=True, blank=True)
    date_fin = models.DateField(null=True, blank=True)
    chef_projet = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='projets_auteur',
    )

    collaborateurs = models.ManyToManyField(
        User,
        through='ProjetCollaborateur',
        related_name='projets_collaborateur',
        blank=True,
    )
    cree_le = models.DateTimeField(auto_now_add=True)
    modifie_le = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nom


class ProjetCollaborateur(models.Model):
    ROLE_CHOICES = [
        ('chef', 'Chef de projet'),
        ('contributeur', 'Contributeur'),
    ]

    projet = models.ForeignKey(Projet, on_delete=models.CASCADE, related_name='collaborateurs_relations')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='contributeur')

    class Meta:
        unique_together = ('projet', 'user')

    def __str__(self):
        return f"{self.user.username} ({self.role}) sur {self.projet.nom}"
