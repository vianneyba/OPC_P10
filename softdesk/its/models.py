from django.db import models
from authenticate.models import User


TAG = (
    ('bug', 'bug'),
    ('improvement', 'improvement'),
    ('task', 'task')
)

STATUS = (
    ('to_do', 'to do'),
    ('in_progress', 'in progress'),
    ('finished', 'finished')
)

TYPE = (
    ('backend', 'backend'),
    ('frontend', 'frontend'),
    ('ios', 'ios'),
    ('android', 'android')
)

PRIORITY = (
    ('FAIBLE', 'FAIBLE'),
    ('MOYENNE', 'MOYENNE'),
    ('ÉLEVÉE', 'ÉLEVÉE')
)

PERMISSIONS_CHOICES = (
        ("author", "author"),
        ("contributor", "contributor"),
)


class Issue(models.Model):
    title = models.CharField(
        max_length=100,
        blank=False)

    description = models.TextField(
        max_length=1500,
        blank=False)

    author = models.ForeignKey(
        User,
        related_name='user',
        on_delete=models.CASCADE)

    tag = models.CharField(
        choices=TAG,
        max_length=20,
        blank=False)

    priority = models.CharField(
        choices=PRIORITY,
        max_length=20,
        blank=False
    )

    status = models.CharField(
        choices=STATUS,
        max_length=20,
        blank=False)

    project = models.ForeignKey(
        'Project',
        related_name='issues',
        on_delete=models.CASCADE)

    created_at = models.DateTimeField(
        auto_now_add=True)

    def __str__(self):
        return f'{self.title}'


class Project(models.Model):
    title = models.CharField(
        max_length=100,
        blank=False)

    description = models.TextField(
        max_length=1500,
        blank=False)

    type = models.CharField(
        choices=TYPE,
        max_length=20,
        blank=False)

    author = models.ForeignKey(
        User,
        related_name='project_author',
        on_delete=models.CASCADE)

    contributors = models.ManyToManyField(
        User,
        through='Contributor',
        related_name='contributions')

    def __str__(self):
        return f'{self.title}'


class Comment(models.Model):
    description = models.TextField(
        max_length=1500,
        blank=False)

    issue = models.ForeignKey(
        'Issue',
        related_name='comments',
        on_delete=models.CASCADE)

    author = models.ForeignKey(
        User,
        related_name='comment_author',
        on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.issue.title}'


class Contributor(models.Model):
    user = models.ForeignKey(
        User,
        related_name='contrib',
        on_delete=models.CASCADE)
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE)

    permission = models.CharField(
        max_length=250,
        choices=PERMISSIONS_CHOICES)
    role = models.CharField(max_length=250)
