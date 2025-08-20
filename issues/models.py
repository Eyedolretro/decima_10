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
    nom = models.CharField(
        max_length=255,
        help_text="Nom du projet"
    )
    description = models.TextField(
        help_text="Description détaillée du projet"
    )
    type = models.CharField(
        max_length=50,
        help_text="Type de projet"
    )
    date_debut = models.DateField(
        null=True, blank=True,
        help_text="Date de début du projet (optionnel)"
    )
    date_fin = models.DateField(
        null=True, blank=True,
        help_text="Date de fin du projet (optionnel)"
    )
    chef_projet = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='projets_chef',
        help_text="Utilisateur responsable du projet"
    )
    collaborateurs = models.ManyToManyField(
        User,
        related_name='projets_collaborateur',
        blank=True,
        help_text="Liste des collaborateurs"
    )

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
