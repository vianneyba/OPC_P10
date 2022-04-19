from django.contrib.auth.models import User
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.response import Response
from its.models import Project, Issue, Comment
from its.serializers import (
    ProjectSerializer, IssueSerializer, CommentSerializer
)
from authenticate.serializers import UserSerializer

USER_NO_EXIST = Response(
    {"message": "user does not exist"},
    status=status.HTTP_404_NOT_FOUND)

PROJECT_NO_EXIST = Response(
    {"message": "project does not exist"},
    status=status.HTTP_404_NOT_FOUND)

CONTRIBUTOR_ADD = Response(
    {"message": "contributor added"}, status=status.HTTP_200_OK)

CONTRIBUTOR_DELETE = Response(
    {"message": "contributor deleted"}, status=status.HTTP_200_OK)

ISSUE_NOT_EXIST = Response(
    {"message": "issue does not exist"},
    status=status.HTTP_404_NOT_FOUND)


class ProjectViewset(ModelViewSet):

    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Project.objects.all()

    def create(self, request, *args, **kwargs):
        tempdict = request.data.copy()
        tempdict['author'] = self.request.user.id
        serializer = self.serializer_class(data=tempdict)

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk, *args, **kwargs):
        try:
            project_instance = Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        tempdict = request.data.copy()
        tempdict['author'] = self.request.user.id

        serializer = ProjectSerializer(
            project_instance,
            data=tempdict)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk, *args, **kwargs):
        try:
            project_instance = Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        project_instance.delete()
        return Response({
            "message": "project deleted"}, status=status.HTTP_200_OK)


class IssueViewset(ModelViewSet):

    serializer_class = IssueSerializer

    def create_issue(
                    self, data, user_id, project_id,
                    update=False, instance=None):
        tempdict = data.copy()
        tempdict['author'] = user_id
        tempdict['project'] = project_id
        if update:
            serializer = IssueSerializer(instance, data=tempdict)
        else:
            serializer = self.serializer_class(data=tempdict)

        return serializer

    def is_valid(self, serializer):
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        return Issue.objects.filter(project=self.kwargs['project_pk'])

    def create(self, request, *args, **kwargs):
        project_id = self.kwargs['project_pk']
        try:
            project = Project.objects.get(pk=project_id)
        except Project.DoesNotExist:
            return PROJECT_NO_EXIST

        serializer = self.create_issue(
            request.data, request.user.id, project_id)

        return self.is_valid(serializer)

    def update(self, request, pk, *args, **kwargs):
        project_id = self.kwargs['project_pk']
        issue_id = self.kwargs['pk']
        try:
            project = Project.objects.get(pk=project_id)
        except Project.DoesNotExist:
            return PROJECT_NO_EXIST

        try:
            issue = Issue.objects.get(pk=issue_id)
        except Issue.DoesNotExist:
            return ISSUE_NOT_EXIST

        serializer = self.create_issue(
            request.data, request.user.id, project_id,
            update=True, instance=issue)

        return self.is_valid(serializer)


class CommentViewSet(ModelViewSet):

    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(issues=self.kwargs['issue_pk'])


class UserViewSet(ModelViewSet):

    serializer_class = UserSerializer

    def get_queryset(self):
        project = Project.objects.get(id=self.kwargs['project_pk'])
        users = list(project.contributors.all())
        users.append(project.author)
        return users

    def create(self, request, *args, **kwargs):
        username = request.data["username"]
        project_id = self.kwargs['project_pk']

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return USER_NO_EXIST

        try:
            project = Project.objects.get(pk=project_id)
        except Project.DoesNotExist:
            return PROJECT_NO_EXIST

        project.contributors.add(user)

        return CONTRIBUTOR_ADD

    def destroy(self, request, pk, *args, **kwargs):
        id_user = self.kwargs['pk']
        id_project = self.kwargs['project_pk']

        try:
            project = Project.objects.get(pk=id_project)
        except Project.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            user = User.objects.get(pk=id_user)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if user in project.contributors.all():
            project.contributors.remove(user)
            project.save()
            return CONTRIBUTOR_DELETE
        else:
            return Response(
                {"message": "user not in project"},
                status=status.HTTP_404_NOT_FOUND)
