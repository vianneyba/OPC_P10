from django.contrib import admin
from authenticate.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'email', 'first_name', 'last_name')


admin.site.register(User, UserAdmin)
