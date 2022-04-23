from rest_framework.serializers import ModelSerializer, SerializerMethodField

from its.models import Project, Issue, Comment
from authenticate.serializers import UserSerializer


class ProjectSerializer(ModelSerializer):

    # contributors = UserSerializer(many=True)
    # author = UserSerializer()
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

    # author = UserSerializer()

    class Meta:
        model = Issue
        fields = [
            'id', 'title', 'description',
            'author', 'tag', 'status',
            'created_at', 'project', 'priority'
        ]


class CommentSerializer(ModelSerializer):

    # author = UserSerializer()

    class Meta:
        model = Comment
        fields = [
            'id', 'description', 'author', 'issue'
        ]
