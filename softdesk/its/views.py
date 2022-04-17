from rest_framework.viewsets import ModelViewSet
from its.models import Project
from its.serializers import ProjectSerializer


class ProjectViewset(ModelViewSet):

    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Project.objects.all()
