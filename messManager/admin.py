from django.contrib import admin
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from messManager.models import Question,Choice


class Manage_Permissions(admin.ModelAdmin):
    search_fields = ['name']
    ordering = ('name',)
    list_display = ('name', 'codename')

    def has_add_permission(self, request):
        return True

    def has_delete_permission(self, request, obj=None):
        return True

class Manage_ContentType(admin.ModelAdmin):
    search_fields = ['name']
    ordering = ('name',)
    list_display = ('name', 'model')

    def has_add_permission(self, request):
        return True

    def has_delete_permission(self, request, obj=None):
        return True

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question_text']

admin.site.register(Question, QuestionAdmin)
admin.site.register(Permission, Manage_Permissions)
admin.site.register(ContentType, Manage_ContentType)