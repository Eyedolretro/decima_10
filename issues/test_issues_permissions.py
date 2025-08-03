from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from issues.models import Projet, Issue


class IssuePermissionsTests(APITestCase):
    def setUp(self):
        # Création des utilisateurs
        self.chef = User.objects.create_user(username="chef", password="pass123")
        self.collab = User.objects.create_user(username="collab", password="pass123")
        self.autre = User.objects.create_user(username="autre", password="pass123")

        # Création d'un projet avec un chef
        self.projet = Projet.objects.create(
            nom="Projet Test",
            description="Description",
            type="backend",
            date_debut="2025-01-01",
            chef_projet=self.chef
        )
        self.projet.collaborateurs.add(self.collab)

        # Création d'un issue lié au projet
        self.issue = Issue.objects.create(
            project=self.projet,
            title="Bug critique",
            description="Description du bug",
            created_by=self.chef
        )

        self.issues_url = reverse("issue-list")  # Nom de la route DRF pour Issue
        self.issue_detail_url = reverse("issue-detail", args=[self.issue.id])

    def test_chef_peut_creer_issue(self):
        self.client.login(username="chef", password="pass123")
        response = self.client.post(self.issues_url, {
            "project": self.projet.id,
            "title": "Nouveau bug",
            "description": "Détails"
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_collaborateur_peut_creer_issue(self):
        self.client.login(username="collab", password="pass123")
        response = self.client.post(self.issues_url, {
            "project": self.projet.id,
            "title": "Bug mineur",
            "description": "Détails"
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_autre_ne_peut_pas_creer_issue(self):
        self.client.login(username="autre", password="pass123")
        response = self.client.post(self.issues_url, {
            "project": self.projet.id,
            "title": "Bug interdit",
            "description": "Détails"
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_chef_peut_modifier_issue(self):
        self.client.login(username="chef", password="pass123")
        response = self.client.patch(self.issue_detail_url, {"title": "Bug corrigé"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_collaborateur_peut_modifier_issue(self):
        self.client.login(username="collab", password="pass123")
        response = self.client.patch(self.issue_detail_url, {"title": "Correction collab"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_autre_ne_peut_pas_modifier_issue(self):
        self.client.login(username="autre", password="pass123")
        response = self.client.patch(self.issue_detail_url, {"title": "Interdit"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_lecture_issue_reserve_aux_membres_projet(self):
        # Chef
        self.client.login(username="chef", password="pass123")
        self.assertEqual(self.client.get(self.issue_detail_url).status_code, status.HTTP_200_OK)

        # Collaborateur
        self.client.login(username="collab", password="pass123")
        self.assertEqual(self.client.get(self.issue_detail_url).status_code, status.HTTP_200_OK)

        # Utilisateur externe
        self.client.login(username="autre", password="pass123")
        self.assertEqual(self.client.get(self.issue_detail_url).status_code, status.HTTP_403_FORBIDDEN)
