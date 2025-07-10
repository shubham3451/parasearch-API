from django.db import models
import uuid
from django.conf import settings


class Paragraph(models.Model):
  """Represents a paragraph of text submitted by a user."""

  id = models.UUIDField(
      primary_key=True, default=uuid.uuid4, editable=False)
  content = models.TextField()
  created_by = models.ForeignKey(
      settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self) -> str:
    """Returns a string representation of the paragraph.

    Returns:
      The ID of the paragraph as a string.
    """
    return f'Paragraph {self.id}'


class WordIndex(models.Model):
  """Maps a normalized word to the paragraph(s) it appears in."""

  word = models.CharField(max_length=100, db_index=True)
  paragraph = models.ForeignKey(Paragraph, on_delete=models.CASCADE)

  class Meta:
    unique_together = ('word', 'paragraph')

  def __str__(self) -> str:
    """Returns a string representation of the word-to-paragraph mapping.

    Returns:
      The word and its associated paragraph ID.
    """
    return f'"{self.word}" in Paragraph {self.paragraph.id}'
