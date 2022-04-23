from rest_framework.permissions import BasePermission
from its.models import Project
from django.db.models import Q


class ProjectPermissions(BasePermission):
    def has_permission(self, request, view):
        message = 'You do not have permission to perform this action.'

        if not request.user.is_authenticated:
            return False

        if view.action in ['update', 'partial_update', 'destroy']:
            try:
                project = Project.objects.get(
                    pk=view.kwargs['pk'], author=request.user)
                return True
            except Project.DoesNotExist:
                return False

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
