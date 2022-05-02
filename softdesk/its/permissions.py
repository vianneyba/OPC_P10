from rest_framework.permissions import BasePermission
from its.models import Project, Issue, Comment, Contributor
from django.db.models import Q


def is_author(project_id, author):
    try:
        Project.objects.get(
            pk=project_id, author=author)
        return True
    except Project.DoesNotExist:
        return False


def is_author_comment(comment_id, author):
    try:
        Comment.objects.get(
            pk=comment_id, author=author)
        return True
    except Comment.DoesNotExist:
        return False


def in_contributors(project_id, user):
    contributor = Contributor.objects.filter(
        project__id=project_id, user=user)
    if contributor.exists():
        return True
    else:
        return False


class ProjectPermissions(BasePermission):

    def has_permission(self, request, view):
        message = 'You do not have permission to perform this action.'

        if not request.user.is_authenticated:
            return False

        if view.action in ['update', 'partial_update', 'destroy']:
            return is_author(view.kwargs['pk'], request.user)

        if view.action in ['retrieve']:
            project = Project.objects.filter(
                Q(contributors=request.user) |
                Q(author=request.user)
            )
            if project.exists():
                return True
            else:
                return False

        return True


class ContributorPermissions(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if view.action in ['list', 'create', 'destroy']:
            return is_author(view.kwargs['project_pk'], request.user)

        return True


class IssuePermissions(BasePermission):
    def is_author(self, issue_id, user):
        try:
            Issue.objects.get(
                pk=issue_id, author=user)
            return True
        except Issue.DoesNotExist:
            return False

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if view.action in ['list', 'create']:
            return in_contributors(
                view.kwargs['project_pk'], request.user)

        if view.action in ['update', 'destroy']:
            return self.is_author(view.kwargs['pk'], request.user)

        return True


class CommentPermissions(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if view.action in ['list', 'create', 'retrieve']:
            return in_contributors(
                view.kwargs['project_pk'], request.user)

        if view.action in ['update', 'destroy']:
            return is_author_comment(view.kwargs['pk'], request.user)

        return True
