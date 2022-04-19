from rest_framework.serializers import ModelSerializer

from its.models import Project, Issue, Comment
from authenticate.serializers import UserSerializer


class ProjectSerializer(ModelSerializer):

    # contributors = UserSerializer(many=True)
    # author = UserSerializer()

    class Meta:
        model = Project
        fields = [
            'id', 'title', 'description',
            'type_project', 'author', 'contributors'
        ]
        extra_kwargs = {
            'contributors': {'allow_empty': True, 'required': False}
        }


class IssueSerializer(ModelSerializer):

    # author = UserSerializer()

    class Meta:
        model = Issue
        fields = [
            'id', 'title', 'description',
            'author', 'tag', 'status',
            'created_at', 'project'
        ]


class CommentSerializer(ModelSerializer):

    author = UserSerializer()

    class Meta:
        model = Comment
        fields = [
            'id', 'description', 'author'
        ]
