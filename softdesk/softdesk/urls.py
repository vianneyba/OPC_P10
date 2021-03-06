from django.contrib import admin
from django.urls import path, include
from rest_framework_nested import routers
from its import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from authenticate.views import SignUpView

router = routers.SimpleRouter()
router.register('projects', views.ProjectViewset, basename='projects')

projects_router = routers.NestedSimpleRouter(
    router, r'projects', lookup='project')
projects_router.register(r'issues', views.IssueViewset, basename='issues')
projects_router.register(r'users', views.UserViewSet, basename='users')

issues_router = routers.NestedSimpleRouter(
    projects_router, r'issues', lookup='issue')
issues_router.register(r'comments', views.CommentViewSet, basename='comments')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('', include(router.urls)),
    path('', include(projects_router.urls)),
    path('', include(issues_router.urls)),
    path('options/', views.option_view, name='options')
]
