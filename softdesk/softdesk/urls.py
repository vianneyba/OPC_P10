from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from its.views import ProjectViewset

router = routers.SimpleRouter()
router.register('projects', ProjectViewset, basename='projects')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('', include(router.urls))
]
