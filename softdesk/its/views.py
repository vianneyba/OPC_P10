from authenticate.models import User
from django.db.models import Q
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from its.models import Project, Issue, Comment
from its.serializers import (
    ProjectSerializer,
    IssueSerializer,
    CommentSerializer,
    ProjectSaveSerializer,
    IssueSaveSerializer,
    CommentSaveSerializer
)
from authenticate.serializers import UserSerializer
from its.permissions import (
    ProjectPermissions,
    ContributorPermissions,
    IssuePermissions,
    CommentPermissions
)

USER_NO_EXIST = Response(
    {"message": "user does not exist"},
    status=status.HTTP_404_NOT_FOUND)

PROJECT_NO_EXIST = Response(
    {"message": "project does not exist"},
    status=status.HTTP_404_NOT_FOUND)

ISSUE_NOT_EXIST = Response(
    {"message": "issue does not exist"},
    status=status.HTTP_404_NOT_FOUND)

COMMENT_NOT_EXIST = Response(
    {"message": "comment does not exist"},
    status=status.HTTP_404_NOT_FOUND)

COMMENT_DELETE = Response(
    {"message": "comment deleted"}, status=status.HTTP_200_OK)

CONTRIBUTOR_DELETE = Response(
    {"message": "contributor deleted"}, status=status.HTTP_200_OK)

CONTRIBUTOR_ADD = Response(
    {"message": "contributor added"}, status=status.HTTP_200_OK)

ISSUE_DELETE = Response(
    {"message": "issue deleted"}, status=status.HTTP_200_OK)

COMMENT_CREATE = Response(
    {"message": "comment created"}, status=status.HTTP_200_OK)

FORBIDDEN = Response(
    status.HTTP_403_FORBIDDEN)


def is_valid(serializer):
    if serializer.is_valid():
        serializer.save()
        return Response(
            serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectViewset(ModelViewSet):

    permission_classes = (IsAuthenticated, ProjectPermissions,)
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Project.objects.filter(
            Q(contributors=self.request.user) |
            Q(author=self.request.user)
        ).distinct()

    def create(self, request, *args, **kwargs):
        tempdict = request.data.copy()
        tempdict['author'] = self.request.user.id
        serializer = ProjectSaveSerializer(data=tempdict)
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

    permission_classes = (IsAuthenticated, IssuePermissions,)
    serializer_class = IssueSerializer

    def create_issue(
                    self, data, user_id, project_id,
                    update=False, instance=None):
        tempdict = data.copy()
        tempdict['author'] = user_id
        tempdict['project'] = project_id
        if update:
            serializer = IssueSaveSerializer(instance, data=tempdict)
        else:
            serializer = IssueSaveSerializer(data=tempdict)

        return serializer

    def get_queryset(self):
        return Issue.objects.filter(project=self.kwargs['project_pk'])

    def create(self, request, *args, **kwargs):
        project_id = self.kwargs['project_pk']
        try:
            Project.objects.get(pk=project_id)
        except Project.DoesNotExist:
            return PROJECT_NO_EXIST

        serializer = self.create_issue(
            request.data, request.user.id, project_id)

        return is_valid(serializer)

    def update(self, request, *args, **kwargs):
        project_id = self.kwargs['project_pk']
        issue_id = self.kwargs['pk']
        try:
            Project.objects.get(pk=project_id)
        except Project.DoesNotExist:
            return PROJECT_NO_EXIST

        try:
            issue = Issue.objects.get(pk=issue_id)
        except Issue.DoesNotExist:
            return ISSUE_NOT_EXIST

        serializer = self.create_issue(
            request.data, request.user.id, project_id,
            update=True, instance=issue)

        return is_valid(serializer)

    def destroy(self, request, *args, **kwargs):
        project_id = self.kwargs['project_pk']
        issue_id = self.kwargs['pk']

        try:
            project = Project.objects.get(pk=project_id)
        except Project.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            issue = Issue.objects.get(pk=issue_id, project=project)
        except Issue.DoesNotExist:
            return ISSUE_NOT_EXIST

        issue.delete()
        return ISSUE_DELETE


class CommentViewSet(ModelViewSet):

    permission_classes = (IsAuthenticated, CommentPermissions,)
    serializer_class = CommentSerializer

    def create_comment(
                    self, data, user_id, issue_id,
                    update=False, instance=None):
        tempdict = data.copy()
        tempdict['author'] = user_id
        tempdict['issue'] = issue_id

        if update:
            serializer = CommentSaveSerializer(instance, data=tempdict)
        else:
            serializer = CommentSaveSerializer(data=tempdict)

        return serializer

    def get_queryset(self):
        return Comment.objects.filter(issue=self.kwargs['issue_pk'])

    def create(self, request, *args, **kwargs):
        project_id = self.kwargs['project_pk']
        issue_id = self.kwargs['issue_pk']

        try:
            issue = Issue.objects.get(pk=issue_id, project__pk=project_id)
        except Issue.DoesNotExist:
            return ISSUE_NOT_EXIST

        serializer = self.create_comment(
            request.data, request.user.id, issue.id)

        return is_valid(serializer)

    def update(self, request, *args, **kwargs):
        comment_id = self.kwargs['pk']
        issue_id = self.kwargs['issue_pk']

        try:
            comment = Comment.objects.get(pk=comment_id)
        except Comment.DoesNotExist:
            return COMMENT_NOT_EXIST

        serializer = self.create_comment(
            request.data, request.user.id, issue_id,
            update=True, instance=comment)

        return is_valid(serializer)

    def destroy(self, request, *args, **kwargs):
        user_id = request.user.id
        comment_id = self.kwargs['pk']

        try:
            comment = Comment.objects.get(pk=comment_id)
        except Comment.DoesNotExist:
            return COMMENT_NOT_EXIST

        if comment.author.id == user_id:
            comment.delete()
        else:
            return FORBIDDEN

        return COMMENT_DELETE


class UserViewSet(ModelViewSet):

    permission_classes = (IsAuthenticated, ContributorPermissions,)
    serializer_class = UserSerializer

    def get_queryset(self):
        project = Project.objects.get(id=self.kwargs['project_pk'])
        users = list(project.contributors.all())
        users.append(project.author)
        return users

    def create(self, request, *args, **kwargs):
        username = request.data["email"]
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
