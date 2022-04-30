from rest_framework.serializers import ModelSerializer

from its import models
from authenticate.serializers import (
    UserSerializer, UserProjectSerializer)


class CommentSaveSerializer(ModelSerializer):

    class Meta:
        model = models.Comment
        fields = [
            'id', 'description', 'author', 'issue'
        ]


class IssueSaveSerializer(ModelSerializer):

    class Meta:
        model = models.Issue
        fields = [
            'id', 'title', 'description',
            'author', 'tag', 'status',
            'created_at', 'project', 'priority'
        ]


class ProjectSaveSerializer(ModelSerializer):

    class Meta:
        model = models.Project
        fields = [
                'id', 'title', 'description',
                'type', 'author', 'contributors']
        extra_kwargs = {
            'contributors': {'allow_empty': True, 'required': False}
        }


class ProjectSerializer(ModelSerializer):

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


class IssueSerializer(ModelSerializer):

    author = UserSerializer(read_only=True)

    class Meta:
        model = models.Issue
        fields = [
            'id', 'title', 'description',
            'author', 'tag', 'status',
            'created_at', 'project', 'priority'
        ]


class CommentSerializer(ModelSerializer):

    author = UserSerializer(read_only=True)

    class Meta:
        model = models.Comment
        fields = [
            'id', 'description', 'author', 'issue'
        ]


class ContributorSaveSerializer(ModelSerializer):

    class Meta:
        model = models.Contributor
        fields = [
            "id", "permission", "role"
        ]


class ContributorSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)
    project = ProjectSerializer(read_only=True)

    class Meta:
        model = models.Contributor
        fields = [
            "id", "user", "project",
            "permission", "role"
        ]
