from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from issues.models import Projet, Issue

User = get_user_model()

class IssuePermissionsTestCase(APITestCase):
    def setUp(self):
        # Création des utilisateurs
        self.chef = User.objects.create_user(username="chef", password="pass123")
        self.contrib = User.objects.create_user(username="contrib", password="pass123")
        self.autre_user = User.objects.create_user(username="autre", password="pass123")

        # Création d’un projet avec chef et contributeur
        self.projet = Projet.objects.create(
            nom="Projet Test",
            description="Description",
            chef_projet=self.chef,
            date_debut="2025-01-01",
            date_fin="2025-12-31"
        )
        self.projet.collaborateurs.add(self.contrib)

        # URL API des issues
        self.url = "/api/issues/"

    def test_non_contributeur_ne_peut_pas_creer_issue(self):
        """Un utilisateur qui n'est pas contributeur ne peut PAS créer une issue"""
        self.client.force_authenticate(user=self.autre_user)  # On force l'authentification

        payload = {
            "title": "Tâche non autorisée",
            "description": "Cet utilisateur ne devrait pas pouvoir créer",
            "project": self.projet.id,
            "priority": "low",
            "status": "open",
            "created_by": self.autre_user.id
        }

        response = self.client.post(self.url, payload, format="json")

        # On s'attend à un 403 Forbidden
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_contributeur_peut_creer_issue(self):
        """Un contributeur peut créer une issue"""
        self.client.force_authenticate(user=self.contrib)

        payload = {
            "title": "Tâche autorisée",
            "description": "Le contributeur peut créer",
            "project": self.projet.id,
            "priority": "low",
            "status": "open",
            "created_by": self.contrib.id
        }

        response = self.client.post(self.url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Issue.objects.filter(title="Tâche autorisée").exists())

    def test_chef_peut_creer_issue(self):
        """Le chef de projet peut créer une issue"""
        self.client.force_authenticate(user=self.chef)

        payload = {
            "title": "Issue chef",
            "description": "Le chef peut créer",
            "project": self.projet.id,
            "priority": "high",
            "status": "open",
            "created_by": self.chef.id
        }

        response = self.client.post(self.url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Issue.objects.filter(title="Issue chef").exists())
