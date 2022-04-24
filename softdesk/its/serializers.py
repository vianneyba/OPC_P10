from rest_framework.serializers import ModelSerializer, SerializerMethodField

from its.models import Project, Issue, Comment
from authenticate.serializers import UserSerializer


class ProjectSaveSerializer(ModelSerializer):

    class Meta:
        model = Project
        fields = [
                'id', 'title', 'description',
                'type_project', 'author', 'contributors']
        extra_kwargs = {
            'contributors': {'allow_empty': True, 'required': False}
        }


class ProjectSerializer(ModelSerializer):

    contributors = UserSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    type = SerializerMethodField('get_type_project')

    class Meta:
        model = Project
        fields = [
            'id', 'title', 'description',
            'type', 'author', 'contributors'
        ]
        extra_kwargs = {
            'contributors': {'allow_empty': True, 'required': False}
        }

    def get_type_project(self, obj):
        return obj.type_project


class IssueSerializer(ModelSerializer):

    author = UserSerializer(read_only=True)

    class Meta:
        model = Issue
        fields = [
            'id', 'title', 'description',
            'author', 'tag', 'status',
            'created_at', 'project', 'priority'
        ]


class CommentSerializer(ModelSerializer):

    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = [
            'id', 'description', 'author', 'issue'
        ]
