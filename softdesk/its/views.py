from authenticate.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from its.models import Project, Issue, Comment, Contributor
from its.models import TYPE, TAG, STATUS, PRIORITY, PERMISSIONS_CHOICES
from its import serializers, permissions, code_return
from authenticate.serializers import UserSerializer


class ProjectViewset(ModelViewSet):

    permission_classes = (IsAuthenticated, permissions.ProjectPermissions,)
    serializer_class = serializers.ProjectSerializer

    def get_queryset(self):
        return Project.objects.filter(
            Q(contributors=self.request.user) |
            Q(author=self.request.user)
        ).distinct()

    def retrieve(self, request, pk=None):
        queryset = Project.objects.all()
        project = get_object_or_404(queryset, pk=pk)
        serializer = serializers.ProjectListSerializer(project)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        tempdict = request.data.copy()
        tempdict['author'] = self.request.user.id
        serializer = serializers.ProjectSaveSerializer(data=tempdict)
        if serializer.is_valid():
            project = serializer.save()
            Contributor.objects.create(
                user=self.request.user,
                project=project,
                permission="author",
                role="auhtor")
            return Response(
                self.serializer_class(project).data,
                status=status.HTTP_201_CREATED)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk, *args, **kwargs):
        try:
            project_instance = Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        tempdict = request.data.copy()

        if 'assign_author' in tempdict:
            tempdict['author'] = tempdict['assign_author']
        else:
            tempdict['author'] = self.request.user.id

        serializer = serializers.ProjectSaveSerializer(
            project_instance, data=tempdict)
        if serializer.is_valid():
            serializer.save()
            return Response(
                self.serializer_class(project_instance).data,
                status=status.HTTP_200_OK)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk, *args, **kwargs):
        try:
            project_instance = Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        project_instance.delete()
        return code_return.PROJECT_DELETE


class IssueViewset(ModelViewSet):

    permission_classes = (IsAuthenticated, permissions.IssuePermissions,)
    serializer_class = serializers.IssueSerializer

    def create_issue(
                    self, data, user_id, project_id,
                    update=False, instance=None):
        tempdict = data.copy()
        tempdict['author'] = user_id
        tempdict['project'] = project_id
        if update:
            serializer = serializers.IssueSaveSerializer(
                instance, data=tempdict)
        else:
            serializer = serializers.IssueSaveSerializer(data=tempdict)

        return serializer

    def get_queryset(self):
        return Issue.objects.filter(project=self.kwargs['project_pk'])

    def retrieve(self, request, *args, **kwargs):
        print(f'pk = {self.kwargs}')
        queryset = Issue.objects.all()
        issue = get_object_or_404(queryset, pk=self.kwargs['pk'])
        serializer = serializers.IssueListSerializer(issue)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        project_id = self.kwargs['project_pk']
        try:
            Project.objects.get(pk=project_id)
        except Project.DoesNotExist:
            return code_return.PROJECT_NO_EXIST

        serializer = self.create_issue(
            request.data, request.user.id, project_id)

        return self.is_valid(serializer)

    def update(self, request, *args, **kwargs):
        project_id = self.kwargs['project_pk']
        issue_id = self.kwargs['pk']
        try:
            Project.objects.get(pk=project_id)
        except Project.DoesNotExist:
            return code_return.PROJECT_NO_EXIST

        try:
            issue = Issue.objects.get(pk=issue_id)
        except Issue.DoesNotExist:
            return code_return.ISSUE_NOT_EXIST

        serializer = self.create_issue(
            request.data, request.user.id, project_id,
            update=True, instance=issue)

        return self.is_valid(serializer)

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
            return code_return.ISSUE_NOT_EXIST

        issue.delete()
        return code_return.ISSUE_DELETE

    def is_valid(self, serializer):
        if serializer.is_valid():
            serializer.save()
            issue = Issue.objects.get(pk=serializer.data['id'])
            issue_sz = serializers.IssueSerializer(issue)
            return Response(
                issue_sz.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentViewSet(ModelViewSet):

    permission_classes = (IsAuthenticated, permissions.CommentPermissions,)
    serializer_class = serializers.CommentSerializer

    def create_comment(
                    self, data, user_id, issue_id,
                    update=False, instance=None):
        tempdict = data.copy()
        tempdict['author'] = user_id
        tempdict['issue'] = issue_id

        if update:
            serializer = serializers.CommentSaveSerializer(
                instance, data=tempdict)
        else:
            serializer = serializers.CommentSaveSerializer(data=tempdict)

        return serializer

    def get_queryset(self):
        return Comment.objects.filter(issue=self.kwargs['issue_pk'])

    def create(self, request, *args, **kwargs):
        project_id = self.kwargs['project_pk']
        issue_id = self.kwargs['issue_pk']

        try:
            issue = Issue.objects.get(pk=issue_id, project__pk=project_id)
        except Issue.DoesNotExist:
            return code_return.ISSUE_NOT_EXIST

        serializer = self.create_comment(
            request.data, request.user.id, issue.id)

        return self.is_valid(serializer)

    def update(self, request, *args, **kwargs):
        comment_id = self.kwargs['pk']
        issue_id = self.kwargs['issue_pk']

        try:
            comment = Comment.objects.get(pk=comment_id)
        except Comment.DoesNotExist:
            return code_return.COMMENT_NOT_EXIST

        serializer = self.create_comment(
            request.data, request.user.id, issue_id,
            update=True, instance=comment)

        return self.is_valid(serializer)

    def destroy(self, request, *args, **kwargs):
        user_id = request.user.id
        comment_id = self.kwargs['pk']

        try:
            comment = Comment.objects.get(pk=comment_id)
        except Comment.DoesNotExist:
            return code_return.COMMENT_NOT_EXIST

        if comment.author.id == user_id:
            comment.delete()
        else:
            return code_return.FORBIDDEN

        return code_return.COMMENT_DELETE

    def is_valid(self, serializer):
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(ModelViewSet):

    permission_classes = (IsAuthenticated, permissions.ContributorPermissions,)
    serializer_class = UserSerializer

    def get_queryset(self):
        users = User.objects.filter(contributions=self.kwargs['project_pk'])
        return users

    def list(self, request, *args, **kwargs):
        contributors = Contributor.objects.filter(project=self.kwargs['project_pk'])
        serializer = serializers.ContributorSerializer(contributors, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        email = request.data["email"]
        project_id = self.kwargs['project_pk']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return code_return.USER_NO_EXIST

        try:
            project = Project.objects.get(pk=project_id)
        except Project.DoesNotExist:
            return code_return.PROJECT_NO_EXIST

        sz = serializers.ContributorSaveSerializer(data=request.data)
        if sz.is_valid():
            try:
                contributor = Contributor.objects.get(
                    user=user, project=project)
                if contributor.permission != request.data['permission']:
                    contributor = Contributor.objects.get(
                        project=project, user=user)
                    contributor.permission = request.data['permission']
                    author_contributor = Contributor.objects.get(
                            project=project, permission='author')
                    author_contributor.permission = 'contributor'
                    author_contributor.save()
                    contributor.save()
                    contributor_sz = serializers.ContributorSerializer(contributor)
                    if request.data['permission'] == 'author':
                        project.author = user
                        project.save()
                    return Response(
                        contributor_sz.data, status=status.HTTP_200_OK)
                return code_return.CONTRIBUTOR_EXISTS
            except Contributor.DoesNotExist:
                sz.save(project=project, user=user)
                contributor = Contributor.objects.get(
                    project=project, user=user)
                contributor_sz = serializers.ContributorSerializer(contributor)
                return Response(
                    contributor_sz.data, status=status.HTTP_200_OK)
        return Response(
            sz.errors, status=status.HTTP_400_BAD_REQUEST)

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

        print(f'user = {user}')

        if user in project.contributors.all():
            project.contributors.remove(user)
            project.save()
            return code_return.CONTRIBUTOR_DELETE
        else:
            return Response(
                {"message": "user not in project"},
                status=status.HTTP_404_NOT_FOUND)


def option_view(self):
    json_object = {
        'tag': TAG,
        'status': STATUS,
        'type': TYPE,
        'priority': PRIORITY,
        'Permissions': PERMISSIONS_CHOICES}

    return JsonResponse(json_object)
