from django.urls import path
from .views import ParagraphUploadView, search_word

urlpatterns = [
    path('paragraphs/upload/', ParagraphUploadView.as_view(), name='paragraph-upload'),
    path('paragraphs/search/', search_word, name='search-word'),
]
