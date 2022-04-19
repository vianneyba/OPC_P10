from django.contrib.auth.models import User
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.response import Response
from its.models import Project, Issue, Comment
from its.serializers import (
    ProjectSerializer, IssueSerializer, CommentSerializer
)
from authenticate.serializers import UserSerializer


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

    def get_queryset(self):
        return Issue.objects.filter(project=self.kwargs['project_pk'])


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
            return Response(
                {"message": "contributor deleted"}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"message": "user not in project"},
                status=status.HTTP_404_NOT_FOUND)
