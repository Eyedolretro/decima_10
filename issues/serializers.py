from rest_framework import serializers
from .models import Issue, Comment

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['author', 'created_at']

class IssueSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Issue
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at']
