from rest_framework.serializers import ModelSerializer

from its.models import Project, Issue, Comment


class ProjectSerializer(ModelSerializer):

    class Meta:
        model = Project
        fields = [
            'id', 'title', 'description',
            'type_project', 'author', 'contributors'
        ]


class IssueSerializer(ModelSerializer):

    class Meta:
        model = Issue
        fields = [
            'id', 'title', 'description',
            'author', 'tag', 'status',
            'created_at'
        ]


class CommentSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = [
            'id', 'description', 'author'
        ]
