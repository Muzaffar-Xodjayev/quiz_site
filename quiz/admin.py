from django.contrib import admin
from django.utils.html import strip_tags
from tinymce.widgets import TinyMCE
from .models import *
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import User, Group

from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm
from unfold.admin import ModelAdmin, TabularInline


admin.site.unregister(User)
admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    # Forms loaded from `unfold.forms`
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm


class SectionSubjectInline(TabularInline):
    model = SectionSubject
    extra = 1


@admin.register(Section)
class SectionAdmin(ModelAdmin):
    list_display = ('title',)
    inlines = [SectionSubjectInline]


@admin.register(Question)
class SectionAdmin(ModelAdmin):
    list_display = ('id', 'subject', 'text_preview')
    list_display_links = ('id', 'subject')

    formfield_overrides = {
        tinymce_models.HTMLField: {'widget': TinyMCE(attrs={'cols': 80, 'rows': 30})},
    }

    def text_preview(self, obj):
        clean_text = strip_tags(obj.text)
        return clean_text[:50] + ('...' if len(clean_text) > 50 else '')

    text_preview.short_description = 'Question Preview'


@admin.register(Result)
class ResultAdmin(ModelAdmin):
    list_display = ["user", "section", "correct_answers", "score"]
    list_display_links = ["user", "section", "correct_answers", "score"]


admin.site.register(Subject)
# admin.site.register(Answer)
