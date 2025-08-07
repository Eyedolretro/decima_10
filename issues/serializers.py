from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Issue, Comment, Projet

User = get_user_model()

# Serializer utilisateur minimal
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

class IssueSerializer(serializers.ModelSerializer):
    created_by = UserMinimalSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Issue
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at']

    def create(self, validated_data):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError("Utilisateur non authentifié.")

        project = validated_data.get('project')
        user = request.user

        if user != project.chef_projet and not project.collaborateurs.filter(id=user.id).exists():
            raise serializers.ValidationError("Vous n'avez pas le droit de créer une issue sur ce projet.")

        # Ne pas passer created_by deux fois
        validated_data['created_by'] = user

        return super().create(validated_data)

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
