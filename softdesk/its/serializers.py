from rest_framework import serializers
from its import models
from authenticate.serializers import (
    UserSerializer, UserProjectSerializer)


class CommentSaveSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Comment
        fields = [
            'id', 'description', 'author', 'issue'
        ]


class IssueSaveSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Issue
        fields = [
            'id', 'title', 'description',
            'author', 'tag', 'status',
            'created_at', 'project', 'priority'
        ]


class ProjectSaveSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Project
        fields = [
                'id', 'title', 'description',
                'type', 'author', 'contributors']
        extra_kwargs = {
            'contributors': {'allow_empty': True, 'required': False}
        }


class ProjectSerializer(serializers.ModelSerializer):

    contributors = UserProjectSerializer(many=True, read_only=True)
    author = UserProjectSerializer(read_only=True)

    class Meta:
        model = models.Project
        fields = [
            'id', 'title', 'description',
            'type', 'author', 'contributors'
        ]
        extra_kwargs = {
            'contributors': {'allow_empty': True, 'required': False}
        }


class IssueSerializer(serializers.ModelSerializer):

    author = UserProjectSerializer(read_only=True)

    class Meta:
        model = models.Issue
        fields = [
            'id', 'title', 'description',
            'author', 'tag', 'status',
            'created_at', 'project', 'priority'
        ]


class CommentSerializer(serializers.ModelSerializer):

    author = UserSerializer(read_only=True)

    class Meta:
        model = models.Comment
        fields = [
            'id', 'description', 'author', 'issue'
        ]


class ContributorSaveSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Contributor
        fields = [
            "id", "permission", "role"
        ]


class ContributorSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    project = serializers.StringRelatedField()

    class Meta:
        model = models.Contributor
        fields = [
            "id", "user", "project",
            "permission", "role"
        ]
