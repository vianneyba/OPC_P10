from django.contrib import admin
from django.urls import path, include
from rest_framework_nested import routers
from its.views import ProjectViewset, IssueViewset

router = routers.SimpleRouter()
router.register('projects', ProjectViewset, basename='projects')

projects_router = routers.NestedSimpleRouter(
    router, r'projects', lookup='project')
projects_router.register(r'issues', IssueViewset, basename='issues')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('', include(router.urls)),
    path('', include(projects_router.urls))
]
