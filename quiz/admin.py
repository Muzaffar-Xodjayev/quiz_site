from django.contrib import admin
from django.contrib.admin import TabularInline
from django.utils.html import strip_tags
from tinymce.widgets import TinyMCE

from .models import *


# class QuestionTabular(TabularInline):
#     model = Question
#     extra = 1
#
#
# @admin.register(Subject)
# class QuestionAdmin(admin.ModelAdmin):
#     list_display = ["id", "name"]
#     list_display_links = ["id", "name"]
#     inlines = [QuestionTabular]



class SectionSubjectInline(admin.TabularInline):
    model = SectionSubject
    extra = 1


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('title',)
    inlines = [SectionSubjectInline]


@admin.register(Question)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'text_preview')
    list_display_links = ('id', 'subject')

    formfield_overrides = {
        tinymce_models.HTMLField: {'widget': TinyMCE(attrs={'cols': 80, 'rows': 30})},
    }

    def text_preview(self, obj):
        clean_text = strip_tags(obj.text)
        return clean_text[:50] + ('...' if len(clean_text) > 50 else '')

    text_preview.short_description = 'Question Preview'


admin.site.register(Subject)
# admin.site.register(SectionSubject)
# admin.site.register(Option)
admin.site.register(Result)
admin.site.register(Answer)
