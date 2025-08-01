from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Issue, Comment, Projet

User = get_user_model()

class UserMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

# Serializer complet utilisateur (si besoin)
class UserMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

# Serializer Commentaire
class CommentSerializer(serializers.ModelSerializer):
    author = UserMinimalSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['author', 'created_at']

# Serializer Issue avec les commentaires imbriqués
class IssueSerializer(serializers.ModelSerializer):
    created_by = UserMinimalSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Issue
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at']

# Serializer inscription utilisateur
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        return user

class ProjetSerializer(serializers.ModelSerializer):
    chef_projet = UserMinimalSerializer(read_only=True)  # lecture seule (assigné automatiquement)
    collaborateurs = UserMinimalSerializer(many=True, read_only=True)
    collaborateurs_ids = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True,
        source='collaborateurs',
        write_only=True,
        required=False
    )

    class Meta:
        model = Projet
        fields = ['id', 'nom', 'description', 'type', 'date_debut', 'date_fin', 'chef_projet', 'collaborateurs', 'collaborateurs_ids']
