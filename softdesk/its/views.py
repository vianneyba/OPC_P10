from rest_framework.viewsets import ModelViewSet
from its.models import Project, Issue, Comment
from its.serializers import (
    ProjectSerializer, IssueSerializer, CommentSerializer
)


class ProjectViewset(ModelViewSet):

    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Project.objects.all()


class IssueViewset(ModelViewSet):

    serializer_class = IssueSerializer

    def get_queryset(self):
        return Issue.objects.filter(project=self.kwargs['project_pk'])


class CommentViewSet(ModelViewSet):

    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(issues=self.kwargs['issue_pk'])
