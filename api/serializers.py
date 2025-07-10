from rest_framework import serializers
from .models import Paragraph


class ParagraphUploadSerializer(serializers.Serializer):
    """Serializer for uploading raw text with multiple paragraphs.

    Paragraphs must be separated by **two newline characters** (i.e., one blank line).

    Example input:
      Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor...
      
      Maecenas volutpat blandit aliquam etiam erat velit scelerisque...
    """

    text = serializers.CharField(
        help_text="Text containing multiple paragraphs separated by blank lines (\\n\\n).",
        style={'base_template': 'textarea.html'}
    )


class ParagraphSerializer(serializers.ModelSerializer):
    """Serializer for displaying a paragraph and its metadata.

    Example:
      {
        "id": "2c14d70e-f74d-4cba-bdee-69e25e6fef0a",
        "content": "Lorem ipsum dolor sit amet.",
        "created_by": "john@example.com",
        "created_at": "2025-07-10T12:00:00Z"
      }
    """

    created_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Paragraph
        fields = ['id', 'content', 'created_by', 'created_at']
        read_only_fields = ['id', 'created_by', 'created_at']
