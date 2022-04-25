from django.contrib import admin
from .models import Issue, Project, Comment


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


admin.site.register(Issue, IssueAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Comment, CommentAdmin)
