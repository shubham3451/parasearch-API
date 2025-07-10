from django.contrib import admin
from .models import Paragraph, WordIndex


@admin.register(Paragraph)
class ParagraphAdmin(admin.ModelAdmin):
    """Admin config for Paragraph model."""

    list_display = ('id', 'created_by', 'short_content', 'created_at')
    list_filter = ('created_by', 'created_at')
    search_fields = ('content', 'created_by__email')
    readonly_fields = ('id', 'created_at')
    ordering = ('-created_at',)

    def short_content(self, obj):
        """Returns first 60 characters of the paragraph."""
        return obj.content[:60] + '...' if len(obj.content) > 60 else obj.content

    short_content.short_description = 'Content Preview'


@admin.register(WordIndex)
class WordIndexAdmin(admin.ModelAdmin):
    """Admin config for WordIndex model."""

    list_display = ('word', 'paragraph')
    search_fields = ('word', 'paragraph__content')
    list_filter = ('word',)

