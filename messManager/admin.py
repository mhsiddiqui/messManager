from django.contrib import admin
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType


class Manage_Permissions(admin.ModelAdmin):
    search_fields = ['name']
    ordering = ('name',)
    list_display = ('name', 'codename')

    def has_add_permission(self, request):
        return True

    def has_delete_permission(self, request, obj=None):
        return True

class Manage_ContentType(admin.ModelAdmin):
    search_fields = ['app_label']
    ordering = ('app_label',)
    list_display = ('app_label', 'model')

    def has_add_permission(self, request):
        return True

    def has_delete_permission(self, request, obj=None):
        return True


admin.site.register(Permission, Manage_Permissions)
admin.site.register(ContentType, Manage_ContentType)