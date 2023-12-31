import datetime
import shutil

from django.contrib import admin
from django.urls import path
from django.utils.html import format_html
from django.contrib import messages
from types import SimpleNamespace

from .views import *
from .utils import CategoryModelAdminUtils, MailTemplateModelAdminUtils


# Register your models here.

class BaseModelAdmin(admin.ModelAdmin):
    exclude = ('created_by',)

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super(BaseModelAdmin, self).get_form(request, obj, **kwargs)
        if not obj:
            form.base_fields['code'].initial = self.model.get_code()
        return form

    def save_model(self, request, obj, form, change):
        if hasattr(self, '_pre_save_model'):
            self._pre_save_model(request, obj, form, change)
        obj.created_by = request.user
        response = super(BaseModelAdmin, self).save_model(request, obj, form, change)
        if hasattr(self, '_post_save_model'):
            self._post_save_model(request, obj, form, change)
        return response

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            self.delete_model(request, obj)


@admin.register(Category)
class CategoryModelAdmin(BaseModelAdmin, CategoryModelAdminUtils):
    list_display = ('id', 'app_name', 'name', 'code', 'is_directory_exist',)
    list_filter = ['app_name', 'code']
    actions = ('create_directory', )
    search_fields = ('name', )

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = self.readonly_fields
        if obj:
            readonly_fields += ('created_by', 'is_directory_exist', 'files_in_directory', 'app_name', 'code')
        return readonly_fields

    # actions
    def delete_model(self, request, obj):
        if self._pre_delete_model(request, obj):
            return super(CategoryModelAdmin, self).delete_model(request, obj)
        return None


try:
    from markdownx.admin import MarkdownxModelAdmin
except ModuleNotFoundError:
    MarkdownxModelAdmin = SimpleNamespace

@admin.register(MailTemplate)
class MailTemplateModelAdmin(BaseModelAdmin, MarkdownxModelAdmin, MailTemplateModelAdminUtils):
    actions = ('sync_templates',)
    list_display = ('id', 'name', 'category', 'is_active', 'code', 'template_status',)
    list_filter = ('category__name', 'is_active', 'code',)
    search_fields = ('name', )
    exclude = ('created_by', 'is_active', 'parent_obj')

    template_blocks = ['{% block style %}', '{% block script %}', '{% block content %}']
    template_check_props = {
        'style_props': SimpleNamespace(length_of_start_key=len(template_blocks[0])),
        'script_props': SimpleNamespace(length_of_start_key=len(template_blocks[1])),
        'body_props': SimpleNamespace(length_of_start_key=len(template_blocks[2]))
    }

    def history_view(self, request, object_id, extra_context=None):
        if not request.user.has_perm('can_view_history'):
            return None
        return super(BaseModelAdmin, self).history_view(request, object_id, extra_context)

    def get_queryset(self, request):
        queryset = self.model.objects.all()
        if not request.user.has_perm('can_view_inactive_objects'):
            queryset = queryset.filter(is_active=True)
        return queryset

    def get_readonly_fields(self, request, obj=None):
        fields = self.readonly_fields
        if obj:
            fields += ('created_at', )
            if obj.parent_obj:
                fields += ('parent_obj', )
            if obj.is_active:
                fields += ('template', )
        if request.user.has_perm('can_view_created_by'):
            fields += ('created_by', )
        return fields

    def has_change_permission(self, request, obj=None):
        return (super(MailTemplateModelAdmin, self) or obj.created_by == request.user) and obj.is_active if obj else True

    def get_action_choices(self, request, default_choices=models.BLANK_CHOICE_DASH):
        action_choices = super(MailTemplateModelAdmin, self).get_action_choices(request, default_choices)
        if not request.user.has_perm('can_sync_templates'):
            for count, choice in enumerate(action_choices):
                if choice[0] == 'sync_templates':
                    del action_choices[count]
        return action_choices

    # urls
    def get_urls(self):
        urls = super(MailTemplateModelAdmin, self).get_urls()
        return [path('template-view/<int:template_code>/', mail_template_view)] + urls