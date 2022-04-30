from django.contrib import admin
from its.models import Issue, Project, Comment
from its.models import Contributor


class IssueAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'description', 'author',
        'tag', 'status', 'project',
        'created_at')


class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'description', 'type',
        'author')


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'description', 'issue', 'author')


class ContributorAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'project', 'user', 'permission', 'role')


admin.site.register(Issue, IssueAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Contributor, ContributorAdmin)
